from typing import List, Optional

from django.db import transaction

from project.celery import app
from trading.models import Inventory, Item, Offer, Trade
from users.models import CustomUser


@transaction.atomic
def make_deal(
        item: Item,
        buyer_offer: Offer,
        seller_offer: Offer,
        buyer: CustomUser,
        seller: CustomUser,
        description: Optional[str] = None,
) -> None:
    if buyer_offer.requested_quantity >= seller_offer.requested_quantity:
        quantity = seller_offer.requested_quantity
    else:
        quantity = buyer_offer.requested_quantity

    unit_price = seller_offer.price
    deal_price = int(unit_price) * quantity

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

    if seller_offer.requested_quantity == buyer_offer.requested_quantity:
        seller_offer.is_active = False
        buyer_offer.is_active = False
    elif seller_offer.requested_quantity < buyer_offer.requested_quantity:
        seller_offer.is_active = False
    else:
        buyer_offer.is_active = False

    buyer_offer.requested_quantity -= seller_offer.requested_quantity

    buyer_offer.save()
    seller_offer.save()
    buyer.save()
    seller.save()
    trade.save()


def find_available_sell_offers(
        offer: Offer
) -> List[Offer]:
    """Finds all available offers for the sale of stock sorted by price and then by quantity. """
    available_offers = Offer.objects.filter(
        is_active=True,
        order_type=Offer.OrderType.SOLD,
        item=offer.item,
        requested_quantity__lte=offer.requested_quantity,
        price__lte=offer.price
    ).order_by('price', 'requested_quantity')

    return available_offers


@app.task
def find_best_offers_and_make_deal() -> None:
    """Finds all available offers for the sale of a stock and then makes deal with the lowest available price."""
    active_buy_offers = Offer.objects.filter(
        order_type=Offer.OrderType.BUY,
        is_active=True
    )

    for buy_offer in active_buy_offers:
        for sell_offer in find_available_sell_offers(buy_offer):
            make_deal(
                item=buy_offer.item,
                buyer_offer=buy_offer,
                seller_offer=sell_offer,
                buyer=buy_offer.user,
                seller=sell_offer.user,
            )
