from django.urls import path, include
from rest_framework_nested import routers

from appuser.vues.user.v_public_user import UserPublicViewSet
from appuser.vues.user.v_user import UserViewSet

router = routers.DefaultRouter()
router.register('abonne', UserViewSet, basename="user_abonne")
router.register('public', UserPublicViewSet, basename="user_public")

urlpatterns = [
    path('', include(router.urls)),
]
