# django default import 
from django.urls import path, include

# third-party imports
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

# local imports
from .views import UserViewSet, MyTokenObtainPairView

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),
]
