from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from rest_framework.utils import json

from apps.products.models import Category, Product
from apps.products.serializers import ProductSerializer
from apps.shops.models import Shop
from tests.base_test import BaseAPITestCase


class ProductsListAPITest(BaseAPITestCase):
    """
    Тесты API списка продуктов.

    Этот класс тестирует эндпоинт, возвращающий список продуктов.
    """
    def setUp(self):
        owners = [
            self.auth_user1,
            self.auth_user2,
        ]
        shops = [
            Shop.objects.create(name='Магазин 1', owner=owners[0]),
            Shop.objects.create(name='Магазин 2', owner=owners[1])
        ]
        categories = [
            Category.objects.create(name='Продукты'),
            Category.objects.create(name='Игры'),
        ]
        products = [
            Product.objects.create(name='Продукт 1', price=10, shop=shops[0]),
            Product.objects.create(name='Продукт 2', price=20.2, shop=shops[0]),
            Product.objects.create(name='Продукт 3', price=3.33, shop=shops[1]),

        ]
        products[1].categories.add(categories[0])
        products[2].categories.set(categories)

        self.url = reverse('product-list')

    def test_get_products_list(self):
        """Получение списка продуктов"""
        response = self.client.get(self.url)
        products = Product.objects.all()
        expected_data = ProductSerializer(products, many=True).data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

