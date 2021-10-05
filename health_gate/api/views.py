from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from food.models import Recipe, Comment, Ingredient, Product
from order.models import Order, OrderRecipe, OrderProduct
from rest_framework import viewsets, generics, permissions
from .permissions import CustomerOrderOrReadOnly
from user.serializers import UserSerializer
from order.serializers import OrderListSerializer, OrderDetailSerializer, OrderRecipeSerializer, OrderProductSerializer
from food.serializers import (RecipeListSerializer,
                              RecipeDetailSerializer,
                              IngredientSerializer,
                              CommentSerializer,
                              ProductSerializer)

User = get_user_model()


# ############################################### Рецепты #######################################################
# используем generecs классы т.к. имеем два сериализвтора для Рецептов
class RecipeListView(generics.ListCreateAPIView):
    """
    вывод списка рецептов и создание одного рецепта
    get, post
    """
    # queryset = Recipe.objects.filter(is_active=True)        # получаем все рецепты из БД, которые прошли модерацию
    queryset = Recipe.objects.all()
    serializer_class = RecipeListSerializer


class RecipeDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Для чтения-записи-удаления конечных точек для экземпляра одного рецепта
    обработчик методов get, put, patch и delete
    """
    queryset = Recipe.objects.all()
    serializer_class = RecipeDetailSerializer


class IngredientView(viewsets.ModelViewSet):
    """
    Конечная точка API, позволяющая просматривать, создавать или редактировать ингредиенты рецептов.
    get, post, put, patch, delete
    сортировка по рецептам
    """
    queryset = Ingredient.objects.order_by('recipe')
    serializer_class = IngredientSerializer


class CommentView(viewsets.ModelViewSet):
    """
    Конечная точка API, позволяющая просматривать, создавать или редактировать комментарии к рецептам.
    get, post, put, patch, delete
    сортировка по рецептам
    доступ: вывод комментариев доступен всем авторизованным. Действия над комментами - для админа или создателя
    """
    queryset = Comment.objects.order_by('recipe')
    serializer_class = CommentSerializer


class ProductView(viewsets.ModelViewSet):
    """Просмотр, создание и редактирование Проодуктов"""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


# ############################################### Пользователи #######################################################
class UserView(viewsets.ModelViewSet):
    """
    Конечная точка API, позволяющая просматривать, создавать или редактировать пользователей.
    get, post, put, patch, delete
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        """
        Возвращает список разрешений для доступа к списку пользователей и дейсвтиям над ними
        Список пользователей доступен для авторизованых Юзеров, действия над ними доступны Персоналу (IsAdminUser)
        """
        if self.action == 'list' or self.action == 'retrieve':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]


# ############################################### Заказы #######################################################
class OrderListView(generics.ListCreateAPIView):
    """
    вывод списка заказов и создание одного заказа
    get, post
    доступ: админы и создатель заказа
    """
    queryset = Order.objects.order_by('customer')
    serializer_class = OrderListSerializer


class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Для чтения-записи-удаления конечных точек для экземпляра одного заказ
    обработчик методов get, put, patch и delete
    доступ: админы и создатель заказа
    """
    queryset = Order.objects.all()
    serializer_class = OrderDetailSerializer
    permission_classes = [CustomerOrderOrReadOnly]


class OrderRecipeView(viewsets.ModelViewSet):
    """
    Конечная точка API, позволяющая просматривать, создавать или редактировать рецепты заказа.
    get, post, put, patch, delete
    сортировка по заказам
    доступ: админы и создатель заказа
    """
    queryset = OrderRecipe.objects.order_by('order')
    serializer_class = OrderRecipeSerializer


class OrderProductView(viewsets.ModelViewSet):
    """
    Конечная точка API, позволяющая просматривать, создавать или редактировать продукты заказа.
    get, post, put, patch, delete
    сортировка по заказам
    доступ: админы и создатель заказа
    """
    queryset = OrderProduct.objects.order_by('recipe')
    serializer_class = OrderProductSerializer
