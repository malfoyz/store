from django.urls import include, path
from rest_framework import routers

from apps.orders.views import CartItemViewSet, OrderViewSet
from apps.products.views import CategoryViewSet, ProductViewSet
from apps.shops.views import ShopViewSet


router = routers.DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'shops', ShopViewSet)
router.register(r'products', ProductViewSet)
router.register(r'cart', CartItemViewSet, basename='cart-item')
router.register(r'orders', OrderViewSet, basename='order')


urlpatterns = [
    # path('', include('apps.profiles.urls')),
    path('', include(router.urls)),
]