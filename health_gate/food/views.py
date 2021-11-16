from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from .models import Recipe, Comment, Ingredient, Product, CookStep, Tag, Filter
from rest_framework import viewsets, generics, status
from api.permissions import AuthorComment, RecipeOwner, IsOwnerRecipeIngredients, IsSuperUser

from .serializers import (RecipeListSerializer,
                          RecipeDetailSerializer,
                          IngredientSerializer,
                          CommentSerializer,
                          ProductSerializer,
                          CookStepSerializer,
                          TagSerializer,
                          FilterSerializer)

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


class RecipeViewSet(viewsets.ModelViewSet):
    """
    Дейсвтия над рецептами
    get, post, put, patch, delete
    """
    queryset = Recipe.objects.all()

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

    def get_serializer_class(self):
        """выбор сериализатора в зависимости от применяемого метода"""
        if self.action == 'list' or self.action == 'create':
            return RecipeListSerializer
        return RecipeDetailSerializer

    def create(self, request, *args, **kwargs):
        """переопределение метода для предоставления права создания рецепта только пользователям из группы "bloger" """
        if request.user.groups.filter(name='bloger').exists() or request.user.is_superuser:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return Response({"error": "Рецепты могут создавать пользователи из группы 'bloger' или Суперпользователь"})

    def perform_create(self, serializer):
        """
        при создании рецепта через post запрос текущий юзер становится его создателем
        привязка ингредиентов и шагов приготовления, созданных внутри рецепта.
        """
        serializer.save(owner=self.request.user)                            # сохраняем текущий рецепт

        ingredients_data = self.request.data.pop('ingredients')             # забираем из передаваемых данных список ингредиентов
        recipe = list(Recipe.objects.all())[-1]                             # присваиваем переменной только что созданный рецепт
        for ingredient_data in ingredients_data:                            # перебор всех переданных ингредиентов
            ingredient_data['product'] = Product.objects.get(name=ingredient_data['product'])
            Ingredient.objects.create(recipe=recipe, **ingredient_data)     # создание ингредиента и привязка его к рецепту

        steps_data = self.request.data.pop('steps')                         # забираем из передаваемых данных список шагов приготовления                            # присваиваем переменной только что созданный рецепт
        for step_data in steps_data:                                        # перебор всех переданных шагов
            CookStep.objects.create(recipe=recipe, **step_data)             # создание шага и привязка его к рецепту


class IngredientView(viewsets.ModelViewSet):
    """
    Просмотр, создавание или редактирование ингредиентов рецептов.
    get, post, put, patch, delete
    Сортировка по рецептам
    """
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [IsOwnerRecipeIngredients]

    def get_queryset(self):
        """
        Фильтр ингредиентов рецептов, пользователем которых является текущий Юзер
        Если пользователь суперпользователь, то вывести все ингредиенты всех рецептов
        Иначе вывод только тех шагов, которые относятся к рецептам текущего юзера
        """
        if self.request.user.is_superuser:
            return self.queryset
        return self.queryset.filter(recipe__owner=self.request.user).order_by('recipe')


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
        Если пользователь суперпользователь, то вывести все шаги всех рецептов
        Иначе вывод только тех шагов, которые относятся к рецептам текущего юзера
        """
        if self.request.user.is_superuser:
            return self.queryset
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
    """
    Просмотр, создание и редактирование Проодуктов.
    Сортировка по Магазину
    Доступы: редактировать может только Суперпользователь,
             просмотр доступен авторизованному пальзователю.
    """
    queryset = Product.objects.order_by('shop')
    serializer_class = ProductSerializer

    def get_permissions(self):
        """
        Просмотр продуктов доступен любому авторизованному пользователю
        Какие-либо дейсвтия над продуктами доступны только суперпользователю
        :return: список разрешений
        """
        if self.request.method == 'GET':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsSuperUser]
        return [permission() for permission in permission_classes]


class TagViewSet(viewsets.ModelViewSet):
    """
    Просмотр, создание и редактирование Тэгов.
    Доступы: редактировать может только Суперпользователь,
             просмотр доступен авторизованному пальзователю.
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    def get_permissions(self):
        """
        Просмотр тэгов доступен всем (в т.ч. неавторизованным Пользователям)
        Какие-либо дейсвтия над тэгами доступны только суперпользователю
        :return: список разрешений
        """
        if self.request.method == 'GET':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsSuperUser]
        return [permission() for permission in permission_classes]


class FilterView(generics.ListAPIView):
    """
    Просмотр вложенных тегов, подтипов тегов и их фильтров.
    Доступы: просмотр доступен авторизованному пальзователю.
    """
    serializer_class = FilterSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Filter.objects.all()