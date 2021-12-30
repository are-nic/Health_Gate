import uuid
import base64

from django.core.files.base import ContentFile
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from .models import Recipe, Comment, IngredientRecipe, Product, CookStep, Tag, Filter, Category, Kitchen
from rest_framework import viewsets, generics, status, filters
from api.permissions import AuthorComment, RecipeOwner, IsOwnerRecipeIngredients, IsSuperUser
from drf_multiple_model.views import ObjectMultipleModelAPIView
from rest_framework.pagination import PageNumberPagination

from .serializers import (
    RecipeListSerializer,
    RecipeDetailSerializer,
    RecipeSerializer,
    RecipeCreateSerializer,
    RecipeCategorySerializer,
    KitchenSerializer,
    IngredientRecipeSerializer,
    CommentSerializer,
    ProductSerializer,
    CookStepSerializer,
    TagSerializer,
    FilterSerializer
)

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
        if self.action == 'list':
            return RecipeListSerializer
        elif self.action == 'retrieve':
            return RecipeDetailSerializer
        elif self.action == 'create':
            return RecipeCreateSerializer
        return RecipeSerializer

    def create(self, request, *args, **kwargs):
        """переопределение метода для предоставления права создания рецепта только пользователям из группы "bloger" """
        if request.user.groups.filter(name='blogger').exists() or request.user.is_superuser:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return Response({
            "error": "Рецепты могут создавать пользователи из группы 'blogger' или Суперпользователь"},
            403
        )

    def perform_create(self, serializer):
        """
        При создании рецепта через post запрос текущий юзер становится его создателем
        привязка ингредиентов и шагов приготовления, созданных внутри рецепта.
        """
        recipe = serializer.save(owner=self.request.user)

        IngredientRecipe.objects.bulk_create([IngredientRecipe(**{
            **ingredient,
            "recipe": recipe,
            "product": Product.objects.get(name=ingredient['product']),
        }) for ingredient in self.request.data.get('ingredients')])

        for step_data in self.request.data.get('steps'):
            file_format, image_str = step_data.get('image').split(';base64,')
            ext = file_format.split('/')[-1]

            cook_step = CookStep.objects.create(
                recipe=recipe,
                title=step_data.get('title'),
                description=step_data.get('description'),
                image=ContentFile(base64.b64decode(image_str), name=f'{uuid.uuid4()}.{ext})'),
            )

            cook_step_ingredients = IngredientRecipe.objects.filter(
                recipe=recipe, product__name__in=step_data.get('ingredients')
            )
            cook_step.ingredients.set(ingredient.id for ingredient in cook_step_ingredients)
            cook_step.save()


class IngredientView(viewsets.ModelViewSet):
    """
    Просмотр, создавание или редактирование ингредиентов рецептов.
    get, post, put, patch, delete
    Сортировка по рецептам
    """
    queryset = IngredientRecipe.objects.all()
    serializer_class = IngredientRecipeSerializer
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


class ProductPagePagination(PageNumberPagination):
    page_size = 20
    max_page_size = 20
    page_size_query_param = 'page_size'


class ProductView(viewsets.ModelViewSet):
    """
    Просмотр, создание и редактирование Проодуктов.
    Сортировка по Магазину
    Доступы: редактировать может только Суперпользователь,
             просмотр доступен авторизованному пальзователю.
    """
    queryset = Product.objects.order_by('shop')
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    pagination_class = ProductPagePagination

    def get_permissions(self):
        """
        Просмотр продуктов доступен любому авторизованному пользователю
        Какие-либо действия над продуктами доступны только суперпользователю
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
             просмотр доступен.
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    def get_permissions(self):
        """
        Просмотр тэгов доступен всем (в т.ч. неавторизованным Пользователям)
        Какие-либо действия над тэгами доступны только суперпользователю
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
    Доступы: просмотр доступен всем.
    """
    serializer_class = FilterSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Filter.objects.all()


class CategoryAndKitchenView(ObjectMultipleModelAPIView):
    querylist = [
        {'queryset': Category.objects.all(), 'serializer_class': RecipeCategorySerializer},
        {'queryset': Kitchen.objects.all(), 'serializer_class': KitchenSerializer},
    ]
