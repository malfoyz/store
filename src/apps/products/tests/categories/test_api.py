from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from rest_framework.utils import json

from apps.products.models import Category
from apps.products.serializers import CategorySerializer
from tests.base_test import BaseAPITestCase


class CategoriesListAPITest(APITestCase):
    """
    Тесты API списка категорий.

    Этот класс тестирует эндпоинт, возвращающий список всех категорий.
    """
    def setUp(self):
        Category.objects.create(name='Продукты')
        Category.objects.create(name='Игры', description='Различные игры')
        self.url = reverse('category-list')

    def test_get_categories_list(self):
        """Получение списка категорий"""
        response = self.client.get(self.url)
        categories = Category.objects.all()
        expected_data = CategorySerializer(categories, many=True).data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)


class CategoriesRetrieveAPITest(APITestCase):
    """
    Тесты API получения конкретной категории.

    Этот класс тестирует эндпоинт, возвращающий одну конкретную категорию.
    """
    def setUp(self):
        Category.objects.create(name='Продукты')

    def test_get_existing_category(self):
        """Получение существующей категории"""
        category = Category.objects.first()
        url = reverse('category-detail', kwargs={'pk': category.pk})
        response = self.client.get(url)
        expected_data = CategorySerializer(category).data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def test_get_non_existent_category(self):
        """Получение несуществующей категории"""
        url = reverse('category-detail', kwargs={'pk': 30})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CategoriesCreateAPITest(BaseAPITestCase):
    """
   Тесты API создания категории.

    Этот класс тестирует эндпоинт, создающий категорию.
   """
    def setUp(self):
        self.url = reverse('category-list')
        self.valid_payload = {
            'name': 'Продукты',
        }
        self.non_valid_payload = {
            'name': ''
        }

    def test_create_category_by_non_authenticated_user(self):
        """Создание категории неаутентифицированным пользователем"""
        response = self.client.post(
            path=self.url,
            data=json.dumps(self.valid_payload),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_category_by_authenticated_user(self):
        """Создание категории аутентифицированным пользователем"""
        self.authenticate(self.auth_user1)
        response = self.client.post(
            path=self.url,
            data=json.dumps(self.valid_payload),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_category_by_admin_user_valid(self):
        """Создание категории администратором на основе валидных данных"""
        self.authenticate(self.admin_user)
        response = self.client.post(
            path=self.url,
            data=json.dumps(self.valid_payload),
            content_type='application/json',
        )
        category = Category.objects.first()
        expected_data = CategorySerializer(category).data

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, expected_data)

    def test_create_category_by_admin_user_non_valid(self):
        """Создание категории администратором на основе невалидных данных"""
        self.authenticate(self.admin_user)
        response = self.client.post(
            path=self.url,
            data=json.dumps(self.non_valid_payload),
            content_type='application/json',
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_category_with_non_unique_name(self):
        """Создание категории с неуникальным именем"""
        self.authenticate(self.admin_user)
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


class CategoriesEditAPITest(BaseAPITestCase):
    """
    Тесты API изменения конкретной категории.

    Этот класс тестирует эндпоинт, изменяющий категорию.
    """
    def setUp(self):
        category = Category.objects.create(name='Продукты')
        self.url = reverse('category-detail', kwargs={'pk': category.pk})
        self.valid_payload = {
            'name': 'Роботы',
        }
        self.non_valid_payload = {
            'name': '',
        }

    def test_edit_category_by_non_authenticated_user(self):
        """Изменение категории неаутентифицированным пользователем"""
        response = self.client.put(
            path=self.url,
            data=json.dumps(self.valid_payload),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_edit_category_by_authenticated_user(self):
        """Изменение категории аутентифицированным пользователем"""
        self.authenticate(self.auth_user1)
        response = self.client.put(
            path=self.url,
            data=json.dumps(self.valid_payload),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_edit_category_by_admin_user_valid(self):
        """Изменение категории администратором на основе валидных данных"""
        self.authenticate(self.admin_user)
        response = self.client.put(
            path=self.url,
            data=json.dumps(self.valid_payload),
            content_type='application/json',
        )
        category = Category.objects.first()
        expected_data = CategorySerializer(category).data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def test_edit_category_by_admin_user_non_valid(self):
        """Изменение категории администратором на основе невалидных данных"""
        self.authenticate(self.admin_user)
        response = self.client.put(
            path=self.url,
            data=json.dumps(self.non_valid_payload),
            content_type='application/json',
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_edit_category_with_non_unique_name(self):
        """Изменение имени категории на неуникальное"""
        self.authenticate(self.admin_user)
        name = 'Роботы'
        Category.objects.create(name=name)
        response = self.client.put(
            path=self.url,
            data=json.dumps({'name': name}),
            content_type='application/json',
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_edit_non_existent_category(self):
        """Изменение несуществующей категории"""
        self.authenticate(self.admin_user)
        url = reverse('category-detail', kwargs={'pk': 30})
        response = self.client.put(
            path=url,
            data=json.dumps(self.valid_payload),
            content_type='application/json',
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        

class CategoriesDestroyAPITest(BaseAPITestCase):
    """
    Тесты API удаления конкретной категории.

    Этот класс тестирует эндпоинт, удаляющий категорию.
    """
    def setUp(self):
        self.category_pk = Category.objects.create(name='Продукты').pk
        self.url = reverse('category-detail', kwargs={'pk': self.category_pk})

    def test_destroy_category_by_non_authenticated_user(self):
        """Удаление категории неаутентифицированным пользователем"""
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_destroy_category_by_authenticated_user(self):
        """Удаление категории аутентифицированным пользователем"""
        self.authenticate(self.auth_user1)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_destroy_existing_category_by_admin_user(self):
        """Удаление существующей категории администратором"""
        self.authenticate(self.admin_user)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(Category.DoesNotExist):
            Category.objects.get(pk=self.category_pk)

    def test_destroy_non_existent_category_by_admin_user(self):
        """Удаление несуществующей категории администратором"""
        self.authenticate(self.admin_user)
        url = reverse('category-detail', kwargs={'pk': 30})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

