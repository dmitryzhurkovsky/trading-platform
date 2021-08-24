from django.urls import path

from trading.views import OfferViewSet

urlpatterns = [
    path('offers/', OfferViewSet.as_view())
]
