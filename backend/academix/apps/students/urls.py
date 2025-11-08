# third-party imports
from rest_framework.routers import DefaultRouter;

# local imports
from .views import StudentViewSet;

router = DefaultRouter();
router.register(r"", StudentViewSet, basename='student');

urlpatterns = router.urls;