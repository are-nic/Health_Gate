from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.views import APIView
from food.serializers import RecipeListSerializer, RecipeDetailSerializer, IngredientCreateSerializer

from food.models import Recipe
from rest_framework import viewsets
from user.serializers import UserSerializer

User = get_user_model()


class RecipeListView(APIView):
    """вывод списка рецептов"""

    def get(self, request):
        # recipes = Recipe.objects.filter(is_active=True)        # получаем все рецепты из БД, которые прошли модерацию
        recipes = Recipe.objects.all()                          # получаем все рецепты из БД (queryset)
        serializer = RecipeListSerializer(recipes, many=True)   # передаем в сериалайзер queryset рецептов
        return Response(serializer.data)                        # возвращаем данные сериализатора в JSON'e


class RecipeDetailView(APIView):
    """вывод одного рецепта"""
    def get(self, request, pk):
        recipe = Recipe.objects.get(id=pk)                      # получаем рецепт из БД по id
        serializer = RecipeDetailSerializer(recipe)
        return Response(serializer.data)


class IngredientCreateView(APIView):
    """добавление ингредиента к определенному рецепту"""
    def post(self, request):
        ingredient = IngredientCreateSerializer(data=request.data)
        if ingredient.is_valid():
            ingredient.save()
        return Response(status=201)


class UserView(viewsets.ModelViewSet):
    """
    Конечная точка API, позволяющая просматривать или редактировать пользователей.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer