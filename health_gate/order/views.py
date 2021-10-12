from rest_framework import viewsets, generics

from .models import Order, OrderRecipe, OrderProduct, MealPlanRecipe
from .serializers import (OrderSerializer,
                          OrderListSerializer,
                          OrderDetailSerializer,
                          OrderRecipeSerializer,
                          OrderProductSerializer,
                          MealPlanRecipeSerializer)
from api.permissions import CustomerOrderOrReadOnly
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated

User = get_user_model()


class OrderViewSet(viewsets.ModelViewSet):
    """
    Все методы для работы с заказами.
    Доступ: создание заказа для любого аутентифицированного юзера
            действия над заказами доступны для владельцев заказа или суперпользователю
    """
    serializer_class = OrderSerializer

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [CustomerOrderOrReadOnly]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Order.objects.all()
        else:
            return Order.objects.filter(customer=self.request.user.id)


class OrderRecipeViewSet(viewsets.ModelViewSet):
    """
    Для взаимодействия с рецептами заказа
    get, post, put, patch, delete
    """
    serializer_class = OrderRecipeSerializer

    def get_queryset(self):
        return OrderRecipe.objects.filter(order=self.kwargs['order_pk'])


class OrderListView(generics.ListCreateAPIView):
    """
    вывод списка заказов и создание одного заказа
    get, post
    доступ: Суперпользователь и создатель заказа
    """
    queryset = Order.objects.order_by('customer')
    serializer_class = OrderListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Order.objects.all()
        else:
            return Order.objects.filter(customer=self.request.user.id)


class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Для чтения-записи-удаления конечных точек для экземпляра одного заказ
    обработчик методов get, put, patch и delete
    доступ:
    """
    queryset = Order.objects.all()
    serializer_class = OrderDetailSerializer
    permission_classes = [CustomerOrderOrReadOnly]


class OrderRecipeView(viewsets.ModelViewSet):
    """
    Конечная точка API, позволяющая просматривать, создавать или редактировать рецепты заказа.
    get, post, put, patch, delete
    сортировка по заказам
    доступ:
    """
    queryset = OrderRecipe.objects.order_by('order')
    serializer_class = OrderRecipeSerializer


class OrderProductView(viewsets.ModelViewSet):
    """
    Конечная точка API, позволяющая просматривать, создавать или редактировать продукты заказа.
    get, post, put, patch, delete
    сортировка по заказам
    доступ:
    """
    queryset = OrderProduct.objects.order_by('recipe')
    serializer_class = OrderProductSerializer


class MealPlanRecipeView(viewsets.ModelViewSet):
    """
    Чтение, запись, редактирование, удаление рецептов плана питания
    """
    queryset = MealPlanRecipe.objects.all().order_by('owner')
    serializer_class = MealPlanRecipeSerializer