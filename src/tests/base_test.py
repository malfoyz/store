from typing import Dict, Type

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken


class BaseAPITestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        """Создает аутентифицированного пользователя и администратора"""
        cls.auth_user1 = get_user_model().objects.create_user(email='auth_user1@example.com', password='password')
        cls.auth_user2 = get_user_model().objects.create_user(email='auth_user2@example.com', password='password')
        cls.admin_user = get_user_model().objects.create_superuser(email='admin@example.com', password='password')

    @staticmethod
    def get_jwt_token(user: Type[AbstractUser]) -> Dict[str, str]:
        """
        Возвращает JWT токен для указанного пользователя.

        :param user: Пользователь, JWT токен которого нужно получить.
        :type user: Type[AbstractUser]

        :return: Словарь, содержащий `refresh` и `access` токены.
        :rtype: Dict[str, str]
        """
        if not isinstance(user, AbstractUser):
            raise TypeError("Передан неподходящий класс пользователя")

        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

    def authenticate(self, user: Type[AbstractUser]) -> None:
        """
        Авторизует пользователя через JWT.

        :param user: Пользователь, которого нужно аутентифицировать с помощью JWT.
        :type user: Type[AbstractUser]

        :return: None
        :rtype: None
        """
        if not isinstance(user, AbstractUser):
            raise TypeError("Передан неподходящий класс пользователя")

        tokens = self.get_jwt_token(user)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + tokens['access'])