from rest_framework.routers import SimpleRouter

from trading.views import OfferViewSet

router = SimpleRouter()

router.register(r'offers', OfferViewSet)

urlpatterns = router.urls