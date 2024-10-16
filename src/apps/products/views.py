from drf_spectacular.utils import extend_schema
from rest_framework import filters, viewsets, status
from rest_framework.response import Response

from base.permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer


@extend_schema(tags=["Category"])
class CategoryViewSet(viewsets.ModelViewSet):
    """Набор представлений для просмотра и модификации категорий"""

    permission_classes = [IsAdminOrReadOnly]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


@extend_schema(tags=["Product"])
class ProductViewSet(viewsets.ModelViewSet):
    """Набор представлений для просмотра и модификации продуктов"""

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsOwnerOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = '__all__'

    def create(self, request, *args, **kwargs) -> Response:
        """
        Переопределяет метод создания объекта.

        Добавляет объект запроса в контекст сериализатора.

        :param request: Объект запроса, содержащий все данные HTTP запроса.
        :type request: Request
        :param args: Дополнительные позиционные аргументы.
        :param kwargs: Additional keyword arguments. Дополнительные именованные аргументы.

        :return: Объект ответа с созданными данными.
        :rtype: Response
        """
        serializer = self.get_serializer(data=request.data, context={'request': request})  # добавили контекст
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
