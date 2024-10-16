from typing import List

from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, permissions

from base.permissions import IsOwnerOrAdmin, ReadOnly
from .models import Shop
from .serializers import ShopSerializer


@extend_schema(tags=["Shop"])
class ShopViewSet(viewsets.ModelViewSet):
    """Набор представлений для просмотра и модификации магазинов"""

    queryset = Shop.objects.all()
    serializer_class = ShopSerializer

    def get_permissions(self) -> List[permissions.BasePermission]:
        """
        Определяет и возвращает список разрешений в зависимости от действия.

        :return: Список экземпляров классов разрешений.
        :rtype: List[BasePermission]
        """
        if self.action == 'create':
            permission_classes = [permissions.IsAuthenticated]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsOwnerOrAdmin]
        else:
            permission_classes = [ReadOnly]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer: ShopSerializer) -> None:
        """
        Переопределяет метод создания объекта.

        Автоматически устанавливает текущего пользователя как владельца магазина
        при сохранении объекта в базу данных.

        :param serializer: Экземпляр сериализатора для сохранения данных.
        :type serializer: ShopSerializer

        :return: None
        :rtype: None
        """
        serializer.save(owner=self.request.user)