from django.db import transaction

from project.celery import app
from trading.models import Inventory, Offer, Trade


@transaction.atomic
def make_deal(
        item,
        buyer_offer,
        seller_offer,
        buyer,
        seller,
        quantity,
        unit_price,
        description=None,
):
    deal_price = float(unit_price) * quantity

    buyer_offer.is_active = False
    seller_offer.is_active = False
    buyer.money -= deal_price
    seller.money += deal_price
    buyer_inventory = Inventory.objects.get(
        item=item,
        user=buyer
    )
    seller_inventory = Inventory.objects.get(
        item=item,
        user=seller
    )
    buyer_inventory.quantity += quantity
    seller_inventory.quantity -= quantity

    buyer_inventory.save()
    seller_inventory.save()
    trade = Trade.objects.create(
        item=item,
        buyer=buyer,
        seller=seller,
        quantity=quantity,
        unit_price=unit_price,
        description=description,
        buyer_offer=buyer_offer,
        seller_offer=seller_offer
    )
    buyer_offer.save()
    seller_offer.save()
    buyer.save()
    seller.save()
    trade.save()


@app.task
def find_best_offers_and_make_deal():
    offers = {
        'BUY': [],
        'SOLD': []
    }

    active_offers = Offer.objects.filter(
        is_active=True
    ).all()
    for offer in active_offers:
        offers[offer.OrderType(offer.order_type).name].append(offer)

    for buyer_offer in offers['BUY'][::-1].__iter__():
        for seller_offer in offers['SOLD'][::-1].__iter__():
            if buyer_offer.item == seller_offer.item:
                if buyer_offer.price == seller_offer.price \
                        and buyer_offer.requested_quantity <= seller_offer.requested_quantity:
                    make_deal(
                        item=seller_offer.item,
                        buyer_offer=buyer_offer,
                        seller_offer=seller_offer,
                        buyer=buyer_offer.user,
                        seller=seller_offer.user,
                        quantity=buyer_offer.requested_quantity,
                        unit_price=seller_offer.price
                    )
                    offers['SOLD'].pop()
                    offers['BUY'].pop()
                    break
