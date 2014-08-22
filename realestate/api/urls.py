from rest_framework import routers
from realestate.api.views import PropiedadViewSet

router = routers.DefaultRouter()
router.register(r'propiedades', PropiedadViewSet)
