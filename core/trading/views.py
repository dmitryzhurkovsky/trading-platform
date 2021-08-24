from rest_framework import mixins, generics
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.viewsets import GenericViewSet


from trading.models import Offer, Item
from trading.serializers import OfferSerializer


class OfferViewSet(
    ListModelMixin,
    CreateModelMixin,
    GenericViewSet,
):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
