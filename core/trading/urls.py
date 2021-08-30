from rest_framework.routers import DefaultRouter

from trading.views import (
    CurrencyViewSet,
    InventoryViewSet,
    OfferViewSet,
    TradeViewSet,
    WatchListViewSet
)

router = DefaultRouter()

router.register(r'offers', OfferViewSet, 'offers')
router.register(r'watch-items', WatchListViewSet, basename='watch-items')
router.register(r'currencies', CurrencyViewSet, basename='currencies')
router.register(r'trades', TradeViewSet, basename='trades')
router.register(r'inventories', InventoryViewSet, basename='inventories')

urlpatterns = router.urls
