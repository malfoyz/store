from django.urls import path, include
from rest_framework import routers

from .views import CustomUserViewSet, GroupViewSet


router = routers.DefaultRouter()
router.register(r'users', CustomUserViewSet)
router.register(r'groups', GroupViewSet)


urlpatterns = [
    path('', include(router.urls)),
]