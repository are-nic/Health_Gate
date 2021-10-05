from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from food.models import Recipe, Comment, Ingredient, Product, CookStep
from order.models import Order, OrderRecipe, OrderProduct
from rest_framework import viewsets, generics, permissions
from .permissions import CustomerOrderOrReadOnly, AuthorComment, RecipeOwner
from user.serializers import UserSerializer
from order.serializers import OrderListSerializer, OrderDetailSerializer, OrderRecipeSerializer, OrderProductSerializer
from food.serializers import (RecipeListSerializer,
                              RecipeDetailSerializer,
                              IngredientSerializer,
                              CommentSerializer,
                              ProductSerializer,
                              CookStepSerializer)

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
    permission_classes = [IsAuthenticated]


class RecipeDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Для чтения-записи-удаления конечных точек для экземпляра одного рецепта
    обработчик методов get, put, patch и delete
    """
    queryset = Recipe.objects.all()
    serializer_class = RecipeDetailSerializer
    permission_classes = [RecipeOwner]


class IngredientView(viewsets.ModelViewSet):
    """
    Конечная точка API, позволяющая просматривать, создавать или редактировать ингредиенты рецептов.
    get, post, put, patch, delete
    сортировка по рецептам
    """
    queryset = Ingredient.objects.order_by('recipe')
    serializer_class = IngredientSerializer


class CookStepView(viewsets.ModelViewSet):
    """
    Конечная точка API, позволяющая просматривать, создавать или редактировать шаги приготовления рецептов.
    get, post, put, patch, delete
    сортировка по рецептам
    """
    queryset = CookStep.objects.order_by('recipe')
    serializer_class = CookStepSerializer


class CommentView(viewsets.ModelViewSet):
    """
    Конечная точка API, позволяющая просматривать, создавать или редактировать комментарии к рецептам.
    get, post, put, patch, delete
    сортировка по рецептам
    доступ: чтение и создание комментариев доступен всем авторизованным.
            Действия над комментами - для суперапользователя или автора коммента
    """
    queryset = Comment.objects.order_by('recipe')
    serializer_class = CommentSerializer

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve' or self.action == 'create':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [AuthorComment]
        return [permission() for permission in permission_classes]


class ProductView(viewsets.ModelViewSet):
    """Просмотр, создание и редактирование Проодуктов"""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


# ############################################### Пользователи #######################################################
class UserView(viewsets.ModelViewSet):
    """
    Конечная точка API, позволяющая просматривать, создавать или редактировать пользователей.
    get, post, put, patch, delete
    Неаутентифицированные пользователи могут отправить GET-запрос для получения списка пользователей,
    но он будет пустым, потому что возвращаемый User.objects.filter (id = self.request.user.id) гарантирует,
    что будет возвращена только информация об аутентифицированном пользователе.

    То же самое относится и к другим методам: если аутентифицированный пользователь пытается УДАЛИТЬ
    другой пользовательский объект, будет возвращено: "Не найдено" (поскольку пользователь, к которому он пытается
    получить доступ, отсутствует в наборе запросов).

    Прошедшие проверку пользователи могут делать со своими пользовательскими объектами все, что захотят.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return User.objects.all()
        else:
            return User.objects.filter(id=self.request.user.id)

    '''def get_permissions(self):
        """
        Возвращает список разрешений для доступа к списку пользователей и дейсвтиям над ними
        Список пользователей доступен для авторизованых Юзеров, действия над ними доступны Персоналу (IsAdminUser)
        """
        if self.action == 'list' or self.action == 'retrieve':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]'''


# ############################################### Заказы #######################################################
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
