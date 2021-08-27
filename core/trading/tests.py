import pytest

from trading.models import *
from trading.tasks import find_best_offers_and_make_deal
from users.models import CustomUser as User
from rest_framework.test import APIClient


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
        "order_type": "b",
        "price": 1000

    })
    assert request.status_code == 400

    request = client.post(path='/api/v1/offers/', data={
        "user": buyer.id,
        "item": item.id,
        "requested_quantity": 1,
        "order_type": "b",
        "price": 2000

    })
    assert request.status_code == 400

    request = client.post(path='/api/v1/offers/', data={
        "user": seller.id,
        "item": item.id,
        "requested_quantity": 2,
        "order_type": "s",
        "price": 1000

    })
    assert request.status_code == 400

    request = client.post(path='/api/v1/offers/', data={
        "user": seller.id,
        "item": item.id,
        "requested_quantity": 1,
        "order_type": "s",
        "price": 1000

    })
    assert request.status_code == 201

    request = client.post(path='/api/v1/offers/', data={
        "user": seller.id,
        "item": item.id,
        "requested_quantity": 1,
        "order_type": "b",
        "price": 1000

    })
    assert request.status_code == 201


@pytest.mark.django_db
def test_find_best_offers_task():
    currency = Currency.objects.create(code='USD', name='United State Dollar')
    item = Item.objects.create(code='AAPL', name='Apple', price=200, currency=currency)

    buyer = User.objects.create(username='buyer', password='some', money=1000)
    seller = User.objects.create(username='seller', password='some', money=5000)
    assert User.objects.count() == 2

    Inventory.objects.create(user=buyer, item=item, quantity=2)
    Inventory.objects.create(user=seller, item=item, quantity=3)
    assert Inventory.objects.count() == 2

    buyer_offer = Offer.objects.create(user=buyer, item=item, requested_quantity=2, order_type='b', price=200)
    seller_offer = Offer.objects.create(user=seller, item=item, requested_quantity=2, order_type='s', price=200)

    find_best_offers_and_make_deal()
    assert User.objects.get(id=buyer.id).money == 600
    assert Inventory.objects.get(
        id=buyer.id,
        item=item
    ).quantity == 4
    assert User.objects.get(id=seller.id).money == 5400
    assert Inventory.objects.get(
        id=seller.id,
        item=item
    ).quantity == 1
    assert Offer.objects.get(id=buyer_offer.id).is_active == False
    assert Offer.objects.get(id=seller_offer.id).is_active == False
    assert Trade.objects.count() == 1


# @pytest.mark.django_db
# def test_trade():
#     """draft"""
#     currency = Currency.objects.create(code='USD', name='United State Dollar')
#     item = Item.objects.create(code='AAPL', name='Apple', price=200, currency=currency)
#
#     buyer = User.objects.create(username='buyer', password='some', money=1000)
#     seller = User.objects.create(username='seller', password='some', money=5000)
#     assert User.objects.count() == 2
#
#     Inventory.objects.create(user=buyer, item=item, quantity=2)
#     Inventory.objects.create(user=seller, item=item, quantity=3)
#     assert Inventory.objects.count() == 2
#
#     buyer_offer = Offer.objects.create(user=buyer, item=item, requested_quantity=2, order_type='b', price=200)
#     seller_offer = Offer.objects.create(user=seller, item=item, requested_quantity=2, order_type='s', price=200)
#
#     client = APIClient()
#
#     request = client.post(path='/api/v1/trades/', data={
#         "item": item.id,
#         "buyer": buyer.id,
#         "seller": seller.id,
#         "quantity": 2,
#         "unit_price": 200,
#         "buyer_offer": buyer_offer.id,
#         "seller_offer": seller_offer.id
#     })
#     assert request.status_code == 201
#
#     assert User.objects.get(id=buyer.id).money == 600
#     assert Inventory.objects.get(
#         id=buyer.id,
#         item=item
#     ).quantity == 4
#     assert User.objects.get(id=seller.id).money == 5400
#     assert Inventory.objects.get(
#         id=seller.id,
#         item=item
#     ).quantity == 1
#     assert Offer.objects.get(id=buyer_offer.id).is_active == False
#     assert Offer.objects.get(id=seller_offer.id).is_active == False

