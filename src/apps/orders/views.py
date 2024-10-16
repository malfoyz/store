from typing import List

from django.db.models import QuerySet
from django.db.transaction import atomic
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, permissions, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from .models import CartItem, Order, OrderItem
from .serializers import CartItemSerializer, OrderSerializer


@extend_schema(tags=["CartItem"])
class CartItemViewSet(viewsets.ModelViewSet):
    """Набор представлений для просмотра и модификации элементов корзины"""

    http_method_names = ['get', 'post', 'patch', 'delete']  # убрали PUT, так как обновлять будем только quantity
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self) -> QuerySet[CartItem]:
        """
        Переопределяет метод получения набора запросов элементов корзины.

        Возвращает элементы, которые принадлежат текущему пользователю (request.user).

        :return: Набор запросов элементов корзины, принадлежащих текущему пользователю.
        :rtype: QuerySet[CartItem]
        """
        return CartItem.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs) -> Response:
        """
        Переопределяет метод создания объекта.

        Получает сериализатор для вывода данных в Response:
        1) либо вновь созданного объекта
        2) либо уже существующего объекта.

        :param request: Объект запроса, содержащий все данные HTTP запроса.
        :type request: Request
        :param args: Дополнительные позиционные аргументы.
        :param kwargs: Additional keyword arguments. Дополнительные именованные аргументы.

        :return: Объект ответа с созданными данными.
        :rtype: Response
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer = self.perform_create(serializer)    # текущий сериализатор, либо вновь созданный
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer: CartItemSerializer) -> CartItemSerializer:
        """
        Переопределяет метод создания объекта на основе провалидированных данных.

        - Если у пользователя уже есть элемент корзины с выбранным продуктом,
          то просто добавляется выбранное им количество к уже существующему элементу корзины
          (это сделано, чтобы убрать дублирование).
        - Если нет, то
            - создает новый элемент корзины с выбранным продуктом;
            - автоматически устанавливает текущего пользователя, которому
              принадлежит элемент корзины, при сохранении объекта в базу данных.

        :param serializer: Экземпляр сериализатора для сохранения данных.
        :type serializer: CartItemSerializer

        :return: Экземпляр сериализатора модели.
        :rtype: CartItemSerializer
        """
        product = serializer.validated_data.get('product')
        cart_item = self.get_queryset().filter(product=product).first()
        if cart_item:  # если такой элемент есть, то просто добавляем количество
            cart_item.quantity += serializer.validated_data.get('quantity')
            cart_item.save()
            return CartItemSerializer(instance=cart_item)
        else:
            serializer.save(user=self.request.user)  # если такого элемента нет, то создаем
            return serializer

    def partial_update(self, request, *args, **kwargs) -> Response:
        """
        Переопределяет метод частичного обновления объекта.

        Позволяет изменять только поле `quantity`.

        :param request: Объект запроса, содержащий все данные HTTP запроса.
        :type request: Request
        :param args: Дополнительные позиционные аргументы.
        :param kwargs: Additional keyword arguments. Дополнительные именованные аргументы.

        :return:    Объект ответа с созданными данными.
        :rtype: Response
        """
        if 'quantity' not in request.data or len(request.data) > 1:
            raise ValidationError("You can only update the 'quantity' field.")
        return super().partial_update(request, *args, **kwargs)


@extend_schema(tags=["Order"])
class OrderViewSet(viewsets.ModelViewSet):
    """Набор представлений для просмотра и модификации заказов"""

    serializer_class = OrderSerializer

    def get_queryset(self) -> QuerySet[Order]:
        """
        Переопределяет метод получения набора запросов элементов корзины.

        Возвращает элементы по следующим правилам:
        - для администратора - все записи;
        - для текущего пользователя - только его записи.

        :return: Набор запросов элементов корзины, принадлежащих текущему пользователю.
        :rtype: QuerySet[Order]
        """
        if self.request.user.is_staff:
            return Order.objects.all()
        else:
            return Order.objects.filter(customer=self.request.user)

    def create(self, request, *args, **kwargs) -> Response:
        """
        Переопределяет метод создания объекта.

        Создает заказ на основе данных из корзины пользователя,
        очищая при этом корзину.

        :param request: Объект запроса, содержащий все данные HTTP запроса.
        :type request: Request
        :param args: Дополнительные позиционные аргументы.
        :param kwargs: Additional keyword arguments. Дополнительные именованные аргументы.

        :return: Объект ответа с созданными данными.
        :rtype: Response
        """
        cart_items = CartItem.objects.select_related('product').filter(user=request.user)

        if not cart_items.exists():
            return Response(data={'detail': 'Корзина пустая, нечего добавить'}, status=status.HTTP_400_BAD_REQUEST)

        with atomic():
            order = Order.objects.create(customer=request.user)
            for item in cart_items:
                order_item = OrderItem(order=order, product=item.product, quantity=item.quantity)
                order_item.save()
            cart_items.delete()

        serializer = self.get_serializer(instance=order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_permissions(self) -> List[permissions.BasePermission]:
        """
        Определяет и возвращает список разрешений в зависимости от действия.

        :return: Список экземпляров классов разрешений.
        :rtype: List[BasePermission]
        """
        if self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAdminUser]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]