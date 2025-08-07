from rest_framework.routers import SimpleRouter
from .views import EmployeeViewSet

router = SimpleRouter()
router.register(r'creation', EmployeeViewSet, basename='creation')

urlpatterns = router.urls