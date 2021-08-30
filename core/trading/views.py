from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated

from trading.models import Currency, Inventory, Item, Offer, Trade
from trading.serializers import (
    CurrencySerializer,
    InventorySerializer,
    ItemsSerializer,
    OfferSerializer,
    TradeSerializer,
    WatchListSerializer
)


class OfferViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer


class ItemViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    queryset = Item.objects.all()
    serializer_class = ItemsSerializer


class CurrencyViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer


class TradeViewSet(
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    queryset = Trade.objects.all()
    serializer_class = TradeSerializer


class WatchListViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    permission_classes = (IsAuthenticated,)
    serializer_class = WatchListSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = Item.objects.filter(
            watchlist__user=user
        ).all()
        return queryset


class InventoryViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    permission_classes = (IsAuthenticated,)
    serializer_class = InventorySerializer

    def get_queryset(self):
        user = self.request.user
        queryset = Inventory.objects.filter(
            user=user
        ).all()
        return queryset
