from rest_framework import viewsets, generics

from .models import Order, OrderRecipe, MealPlanRecipe
from food.models import Recipe

from .serializers import (OrderListSerializer,
                          OrderDetailSerializer,
                          OrderRecipeSerializer,
                          # OrderRecipeDetailSerializer,
                          # OrderProductSerializer,
                          MealPlanRecipeSerializer)

from api.permissions import CustomerOrderOrReadOnly
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated

User = get_user_model()


# ---------------------------------------------For Nested Routers--------------------------------------------
class OrderViewSet(viewsets.ModelViewSet):
    """
    Создан для вложенных маршрутов, связанных с Заказом
    Все методы для работы с заказами.
    Доступ: создание заказа для любого аутентифицированного юзера
            действия над заказами доступны для владельцев заказа или суперпользователю
    """

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

    def get_serializer_class(self):
        """выбор сериализатора в зависимости от применяемого метода"""
        if self.action == 'list':
            return OrderListSerializer
        return OrderDetailSerializer

    def perform_create(self, serializer):
        """При создании заказа текущий юзер заносится в поле Customer"""
        recipes = self.request.data.pop('recipes')

        order = Order.objects.create(
            customer=self.request.user,
            name=self.request.data.get('name'),
            address=self.request.data.get('address'),
            phone_number=self.request.data.get('phone_number'),
            pay_method=self.request.data.get('pay_method'),
            at_door=self.request.data.get('at_door'),
        )

        for recipe_data in recipes:
            recipe = Recipe.objects.filter(title=recipe_data.get('recipe')).first()
            OrderRecipe.objects.create(
                recipe=recipe,
                qty=recipe_data.get('qty'),
                order=order
            )


class OrderRecipeViewSet(viewsets.ModelViewSet):
    """
    Создан для вложенных маршрутов, связанных с Заказом
    Для взаимодействия с рецептами заказа
    get, post, put, patch, delete
    """
    serializer_class = OrderRecipeSerializer

    def get_queryset(self):
        return OrderRecipe.objects.filter(order=self.kwargs['orders_pk'])
# ----------------------------------------------------------------------------------------------------------


class OrderRecipeView(viewsets.ModelViewSet):
    """
    Конечная точка API, позволяющая просматривать, создавать или редактировать рецепты заказа.
    get, post, put, patch, delete
    сортировка по заказам
    доступ: Ко всем рецептам заказов в БД имеет доступ Суперпользователь
            Любой пользователь имеет доступ к своим рецептам заказа.
    """
    queryset = OrderRecipe.objects.order_by('order')
    serializer_class = OrderRecipeSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return self.queryset
        return self.queryset.filter(order__customer=self.request.user)


'''
class OrderProductView(viewsets.ModelViewSet):
    """
    Конечная точка API, позволяющая просматривать, создавать или редактировать продукты заказа.
    get, post, put, patch, delete
    сортировка по заказам
    доступ:
    """
    queryset = OrderProduct.objects.order_by('recipe')
    serializer_class = OrderProductSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return self.queryset
        return self.queryset.filter(order__customer=self.request.user)
'''


class MealPlanRecipeView(viewsets.ModelViewSet):
    """
    Чтение, запись, редактирование, удаление рецептов плана питания
    доступ: список всех планов питани и действия над ними для Суперюзера
            для пользователей - вывод только их планов питания и дейсвтия над ними
    """
    queryset = MealPlanRecipe.objects.all().order_by('owner')
    serializer_class = MealPlanRecipeSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return self.queryset
        return self.queryset.filter(owner=self.request.user)

    def perform_create(self, serializer):
        """при создании плана через post запрос текущий юзер становится его создателем"""
        serializer.save(owner=self.request.user)
