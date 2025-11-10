# third-party imports
from rest_framework.routers import DefaultRouter

# local imports
from .views import TeacherViewSet

router = DefaultRouter()
router.register(r'teachers', TeacherViewSet, basename='teacher')

urlpatterns = router.urls
