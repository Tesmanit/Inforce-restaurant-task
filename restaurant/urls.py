from rest_framework.routers import SimpleRouter
from .views import MenuViewSet, RestaurantViewSet

router = SimpleRouter()
router.register(r'menu', MenuViewSet, basename='menu')
router.register(r'creation', RestaurantViewSet, basename='creation')

urlpatterns = router.urls