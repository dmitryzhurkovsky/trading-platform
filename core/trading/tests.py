import pytest
from rest_framework.test import APIClient

from trading.models import Currency, Inventory, Item, Offer, Trade
from trading.tasks import find_best_offers_and_make_deal
from users.models import CustomUser as User


@pytest.mark.django_db
def test_validation_creating_offer():
    currency = Currency.objects.create(code='USD', name='United State Dollar')
    item = Item.objects.create(code='AAPL', name='Apple', price=1000, currency=currency)

    buyer = User.objects.create(username='buyer', password='some', money=1000)
    seller = User.objects.create(username='seller', password='some', money=1000)
    assert User.objects.count() == 2

    Inventory.objects.create(user=buyer, item=item, quantity=1)
    Inventory.objects.create(user=seller, item=item, quantity=1)
    assert Inventory.objects.count() == 2

    client = APIClient()

    request = client.post(path='/api/v1/offers/', data={
        "user": buyer.id,
        "item": item.id,
        "requested_quantity": 2,
        "order_type": Offer.OrderType.BUY.value,
        "price": 1000

    })
    assert request.status_code == 400

    request = client.post(path='/api/v1/offers/', data={
        "user": buyer.id,
        "item": item.id,
        "requested_quantity": 1,
        "order_type": Offer.OrderType.BUY.value,
        "price": 2000

    })
    assert request.status_code == 400

    request = client.post(path='/api/v1/offers/', data={
        "user": seller.id,
        "item": item.id,
        "requested_quantity": 2,
        "order_type": Offer.OrderType.SOLD.value,
        "price": 1000

    })
    assert request.status_code == 400

    request = client.post(path='/api/v1/offers/', data={
        "user": seller.id,
        "item": item.id,
        "requested_quantity": 1,
        "order_type": Offer.OrderType.SOLD.value,
        "price": 1000

    })
    assert request.status_code == 201

    request = client.post(path='/api/v1/offers/', data={
        "user": seller.id,
        "item": item.id,
        "requested_quantity": 1,
        "order_type": 1,
        "price": 1000

    })
    assert request.status_code == 201


@pytest.mark.django_db
def test_find_best_offers_task():
    currency = Currency.objects.create(code='USD', name='United State Dollar')
    apple_stock = Item.objects.create(code='AAPL', name='Apple', price=200, currency=currency)
    tesla_stock = Item.objects.create(code='TSL', name='Tesla', price=200, currency=currency)
    assert Item.objects.count() == 2

    buyer = User.objects.create(username='buyer', password='some', money=5000)
    seller = User.objects.create(username='seller', password='some', money=5000)
    assert User.objects.count() == 2

    Inventory.objects.create(user=buyer, item=apple_stock, quantity=4)
    Inventory.objects.create(user=seller, item=apple_stock, quantity=4)
    Inventory.objects.create(user=buyer, item=tesla_stock, quantity=4)
    Inventory.objects.create(user=seller, item=tesla_stock, quantity=4)
    assert Inventory.objects.count() == 4

    offer_to_buy_apple_stocks = Offer.objects.create(
        user=buyer,
        item=apple_stock,
        requested_quantity=2,
        order_type=Offer.OrderType.BUY.value,
        price=200
    )
    offer_to_sell_apple_stocks = Offer.objects.create(
        user=seller,
        item=apple_stock,
        requested_quantity=2,
        order_type=Offer.OrderType.SOLD.value,
        price=200
    )

    offer_to_buy_tesla_stocks = Offer.objects.create(
        user=buyer,
        item=tesla_stock,
        requested_quantity=2,
        order_type=Offer.OrderType.BUY.value,
        price=200
    )
    offer_to_sell_tesla_stocks = Offer.objects.create(
        user=seller,
        item=tesla_stock,
        requested_quantity=2,
        order_type=Offer.OrderType.SOLD.value,
        price=200
    )

    find_best_offers_and_make_deal()
    assert User.objects.get(id=buyer.id).money == 4200
    assert Inventory.objects.get(
        user=buyer,
        item=apple_stock
    ).quantity == 6
    assert Inventory.objects.get(
        user=buyer,
        item=tesla_stock
    ).quantity == 6
    assert User.objects.get(id=seller.id).money == 5800
    assert Inventory.objects.get(
        user=seller,
        item=apple_stock
    ).quantity == 2
    assert Inventory.objects.get(
        user=seller,
        item=tesla_stock
    ).quantity == 2
    assert Offer.objects.get(id=offer_to_buy_apple_stocks.id).is_active is False
    assert Offer.objects.get(id=offer_to_sell_apple_stocks.id).is_active is False
    assert Offer.objects.get(id=offer_to_buy_tesla_stocks.id).is_active is False
    assert Offer.objects.get(id=offer_to_sell_tesla_stocks.id).is_active is False
    assert Trade.objects.count() == 2
