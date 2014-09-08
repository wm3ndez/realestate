from rest_framework import routers
from realestate.api.views import ListingViewSet

router = routers.DefaultRouter()
router.register(r'listings', ListingViewSet)
