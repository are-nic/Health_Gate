from rest_framework import serializers
from .models import Recipe, Ingredient, Comment


class RecipeListSerializer(serializers.ModelSerializer):
    """Список рецептов"""
    category = serializers.SlugRelatedField(slug_field='name', read_only=True)
    owner = serializers.CharField(source="owner.phone_number", read_only=True)

    class Meta:
        model = Recipe
        fields = ('id', 'owner', 'category', 'title')


class IngredientCreateSerializer(serializers.ModelSerializer):
    """
    Добавление ингредиента
    """
    class Meta:
        model = Ingredient
        exclude = ['id', 'id_product']


class CommentCreateSerializer(serializers.ModelSerializer):
    """
    Добавление комментария к рецепту
    """
    author = serializers.CharField(source="author.phone_number", read_only=True)

    class Meta:
        model = Comment
        exclude = ['id']


class RecipeDetailSerializer(serializers.ModelSerializer):
    """Один рецепт"""
    owner = serializers.CharField(source="owner.phone_number", read_only=True)
    category = serializers.SlugRelatedField(slug_field='name', read_only=True)
    kitchen = serializers.SlugRelatedField(slug_field='name', read_only=True)
    ingredients = IngredientCreateSerializer(many=True)
    tags = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True)
    comments = CommentCreateSerializer(many=True)

    class Meta:
        model = Recipe
        fields = '__all__'