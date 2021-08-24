from rest_framework import mixins, generics

from trading.models import Offer
from trading.serializers import OfferSerializer


class OfferViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    generics.GenericAPIView
):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
