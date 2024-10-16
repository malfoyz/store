from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.utils import json

from apps.shops.models import Shop
from apps.shops.serializers import ShopSerializer
from tests.base_test import BaseAPITestCase


class ShopsListAPITest(BaseAPITestCase):
    """
    Тесты API списка магазинов.

    Этот класс тестирует эндпоинт, возвращающий список всех магазинов.
    """
    def setUp(self):
        owner1, owner2 = self.auth_user1, self.auth_user2
        Shop.objects.create(name='Магазин 1', owner=owner1)
        Shop.objects.create(name='Магазин 2', owner=owner1,
                            description='Продуктовый')
        Shop.objects.create(name='Магазин 3', owner=owner2,
                            description='Продуктовый',
                            address='Адрес')
        self.url = reverse('shop-list')

    def test_get_shops_list_by_anonym_user(self):
        """Получение списка магазинов"""
        response = self.client.get(self.url)
        shops = Shop.objects.all()
        expected_data = ShopSerializer(shops, many=True).data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)


class ShopsRetrieveAPITest(BaseAPITestCase):
    """
    Тесты API получения конкретного магазина.

    Этот класс тестирует эндпоинт, возвращающий один конкретный магазин.
    """
    def setUp(self):
        owner = self.auth_user1
        Shop.objects.create(name='Магазин', owner=owner)

    def test_get_existing_category(self):
        """Получение существующей магазина"""
        shop = Shop.objects.first()
        url = reverse('shop-detail', kwargs={'pk': shop.pk})
        response = self.client.get(url)
        expected_data = ShopSerializer(shop).data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def test_get_non_existent_shop(self):
        """Получение несуществующего магазина"""
        url = reverse('shop-detail', kwargs={'pk': 30})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class ShopsCreateAPITest(BaseAPITestCase):
    """
    Тесты API создания магазина.

    Этот класс тестирует эндпоинт, создающий категорию.
    """
    def setUp(self):
        self.url = reverse('shop-list')
        self.valid_payload = {
            'name': 'Магазин',
        }
        self.non_valid_payload = {
            'name': ''
        }

    def test_create_shop_by_non_authenticated_user(self):
        """Создание магазина неаутентифицированным пользователем"""
        response = self.client.post(
            path=self.url,
            data=json.dumps(self.valid_payload),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_shop_by_authenticated_user_valid(self):
        """Создание магазина аутентифицированным пользователем на основе валидных данных"""
        self.authenticate(self.auth_user1)
        response = self.client.post(
            path=self.url,
            data=json.dumps(self.valid_payload),
            content_type='application/json',
        )
        shop = Shop.objects.first()
        expected_data = ShopSerializer(shop).data

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, expected_data)

    def test_create_shop_by_non_authenticated_user_non_valid(self):
        """Создание категории аутентифицированным пользователем на основе невалидных данных"""
        self.authenticate(self.auth_user1)
        response = self.client.post(
            path=self.url,
            data=json.dumps(self.non_valid_payload),
            content_type='application/json',
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_shop_with_non_unique_name(self):
        """Создание магазина с неуникальным именем"""
        self.authenticate(self.auth_user1)
        self.client.post(
            path=self.url,
            data=json.dumps(self.valid_payload),
            content_type='application/json',
        )
        response = self.client.post(
            path=self.url,
            data=json.dumps(self.valid_payload),
            content_type='application/json',
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ShopsEditAPITest(BaseAPITestCase):
    """
    Тесты API изменения конкретного магазина.

    Этот класс тестирует эндпоинт, изменяющий магазин.
    """
    def setUp(self):
        self.owner = self.auth_user1
        self.other_user = self.auth_user2
        shop = Shop.objects.create(name='Магазин', owner=self.owner)
        self.url = reverse('shop-detail', kwargs={'pk': shop.pk})
        self.valid_payload = {
            'name': 'Измененный магазин',
        }
        self.non_valid_payload = {
            'name': '',
        }

    def test_edit_shop_by_non_authenticated_user(self):
        """Изменение магазина неаутентифицированным пользователем"""
        response = self.client.put(
            path=self.url,
            data=json.dumps(self.valid_payload),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_edit_another_shop_by_authenticated_user(self):
        """Изменение чужого магазина аутентифицированным пользователем"""
        self.authenticate(self.other_user)
        response = self.client.put(
            path=self.url,
            data=json.dumps(self.valid_payload),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_edit_shop_by_owner(self):
        """Изменение магазина его владельцем"""
        self.authenticate(self.owner)
        response = self.client.put(
            path=self.url,
            data=json.dumps(self.valid_payload),
            content_type='application/json',
        )
        shop = Shop.objects.first()
        expected_data = ShopSerializer(shop).data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def test_edit_shop_by_admin_user(self):
        """Изменение магазина администратором"""
        self.authenticate(self.admin_user)
        response = self.client.put(
            path=self.url,
            data=json.dumps(self.valid_payload),
            content_type='application/json',
        )
        shop = Shop.objects.first()
        expected_data = ShopSerializer(shop).data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def test_edit_shop_non_valid(self):
        """Изменение магазина на основе невалидных данных"""
        self.authenticate(self.owner)
        response = self.client.put(
            path=self.url,
            data=json.dumps(self.non_valid_payload),
            content_type='application/json',
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_edit_shop_with_non_unique_name(self):
        """Изменение имени магазина на неуникальное"""
        self.authenticate(self.owner)
        name = 'Магазин 2'
        Shop.objects.create(name=name, owner=self.other_user)
        response = self.client.put(
            path=self.url,
            data=json.dumps({'name': name}),
            content_type='application/json',
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_edit_non_existent_shop(self):
        """Изменение несуществующего магазина"""
        self.authenticate(self.other_user)
        url = reverse('shop-detail', kwargs={'pk': 30})
        response = self.client.put(
            path=url,
            data=json.dumps(self.valid_payload),
            content_type='application/json',
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class ShopsDestroyAPITest(BaseAPITestCase):
    """
    Тесты API удаления конкретной категории.

    Этот класс тестирует эндпоинт, удаляющий категорию.
    """
    def setUp(self):
        self.owner = self.auth_user1
        self.other_user = self.auth_user2
        self.shop_pk = Shop.objects.create(name='Магазин', owner=self.owner).pk
        self.url = reverse('shop-detail', kwargs={'pk': self.shop_pk})

    def test_destroy_shop_by_non_authenticated_user(self):
        """Удаление магазина неаутентифицированным пользователем"""
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_destroy_another_shop_by_authenticated_user(self):
        """Удаление чужого магазина аутентифицированным пользователем"""
        self.authenticate(self.other_user)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_destroy_shop_by_owner(self):
        """Удаление магазина его владельцем"""
        self.authenticate(self.owner)
        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(Shop.DoesNotExist):
            Shop.objects.get(pk=self.shop_pk)

    def test_destroy_shop_by_admin_user(self):
        """Удаление магазина администратором"""
        self.authenticate(self.admin_user)
        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(Shop.DoesNotExist):
            Shop.objects.get(pk=self.shop_pk)

    def test_destroy_non_existent_shop(self):
        """Удаление несуществующего магазина"""
        self.authenticate(self.owner)
        url = reverse('shop-detail', kwargs={'pk': 30})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
