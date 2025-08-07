from rest_framework.routers import SimpleRouter
from .views import MenuViewSet, RestaurantViewSet

router = SimpleRouter()
router.register(r'menu', MenuViewSet, basename='menu')

urlpatterns = router.urls