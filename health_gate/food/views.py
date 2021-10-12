from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Recipe, Comment, Ingredient, Product, CookStep
from rest_framework import viewsets, generics, status
from api.permissions import AuthorComment, RecipeOwner, IsOwnerRecipeIngredients, IsSuperUser

from .serializers import (RecipeListSerializer,
                          RecipeDetailSerializer,
                          IngredientSerializer,
                          CommentSerializer,
                          ProductSerializer,
                          CookStepSerializer)

User = get_user_model()


class RecommendRecipesListView(generics.ListAPIView):
    """
    Вывод списка рекомендованных рецептов в соответствии с тегами Юзера
    Доступен для авторизованных юзеров
    """
    serializer_class = RecipeListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Recipe.objects.filter(tags__name__in=list(user.tags.all())).order_by("date_created")


class RecipeListView(generics.ListCreateAPIView):
    """
    вывод списка рецептов и создание одного рецепта
    get, post
    Запостить рецепт может пользователь из группы "bloger"
    """
    # queryset = Recipe.objects.filter(is_active=True)        # получаем все рецепты из БД, которые прошли модерацию
    queryset = Recipe.objects.all()
    serializer_class = RecipeListSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        if request.user.groups.filter(name='bloger').exists():
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return Response({"error": "Недостаточно прав для создания рецепта"})

    def perform_create(self, serializer):
        """при создании рецепта через post запрос текущий юзер становится его создателем"""
        serializer.save(owner=self.request.user)


class RecipeDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Для чтения-записи-удаления экземпляра одного рецепта
    Обработчик методов get, put, patch и delete
    """
    queryset = Recipe.objects.all()
    serializer_class = RecipeDetailSerializer

    def get_permissions(self):
        """
        Просмотр деталей любого рецепта доступен авторизованному пользователю
        Какие-либо дейсвтия над рецептами доступны владельцам рецептов и суперпользователю
        :return: список разрешений
        """
        if self.request.method == 'GET':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [RecipeOwner]
        return [permission() for permission in permission_classes]


class IngredientView(viewsets.ModelViewSet):
    """
    Просмотр, создавание или редактирование ингредиентов рецептов.
    get, post, put, patch, delete
    Сортировка по рецептам
    """
    serializer_class = IngredientSerializer
    permission_classes = [IsOwnerRecipeIngredients]

    def get_queryset(self):
        """
        Фильтр ингредиентов рецептов, пользователем которых является текущий Юзер
        """
        return Ingredient.objects.all().filter(recipe__owner=self.request.user).order_by('recipe')


class CookStepsByRecipeView(generics.ListCreateAPIView):
    """
    получение списка шагов приготовления по конкретному рецепту
    создание шага приготовления
    """
    queryset = CookStep.objects.all()
    serializer_class = CookStepSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """для получения шагов приготовления по конкретному рецепту"""
        recipe = self.kwargs.get('recipe_pk')
        return self.queryset.filter(recipe_pk=recipe)


class CookStepDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CookStep.objects.all()
    serializer_class = CookStepSerializer


class CookStepView(viewsets.ModelViewSet):
    """
    Конечная точка API, позволяющая просматривать, создавать или редактировать шаги приготовления рецептов.
    get, post, put, patch, delete
    сортировка по рецептам
    """
    queryset = CookStep.objects.all()
    serializer_class = CookStepSerializer

    def get_queryset(self):
        """
        Фильтр шагов приготовления рецепта, пользователем которого является текущий Юзер
        """
        return self.queryset.filter(recipe__owner=self.request.user).order_by('recipe')


class CommentView(viewsets.ModelViewSet):
    """
    Читать, создавать или редактировать комментарии к рецептам.
    get, post, put, patch, delete
    сортировка по рецептам
    доступ: чтение и создание комментариев доступен всем авторизованным.
            Действия над комментами - для суперпользователя или автора коммента
            список всех комментов не является необходимостью, поэтому доступен только суперюзеру
    """
    queryset = Comment.objects.order_by('recipe')
    serializer_class = CommentSerializer

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [IsSuperUser]
        elif self.action == 'retrieve' or self.action == 'create':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [AuthorComment]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        """при создании комментария через POST-запрос текущий юзер становится его создателем"""
        serializer.save(author=self.request.user)


class ProductView(viewsets.ModelViewSet):
    """Просмотр, создание и редактирование Проодуктов"""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer