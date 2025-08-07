from rest_framework.routers import SimpleRouter
from .views import MenuViewSet, RestaurantViewSet, VotesViewSet

router = SimpleRouter()
router.register(r"menu", MenuViewSet, basename="menu")
router.register(r"creation", RestaurantViewSet, basename="creation")
router.register(r"votes", VotesViewSet, basename="votes")


urlpatterns = router.urls
