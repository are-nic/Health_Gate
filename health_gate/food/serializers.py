from rest_framework import serializers
from .models import Recipe, Ingredient, Comment, Product


class IngredientSerializer(serializers.ModelSerializer):
    """
    Добавление ингредиента
    """
    class Meta:
        model = Ingredient
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    """
    Добавление комментария к рецепту
    """
    author = serializers.CharField(source="author.phone_number", read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'


class RecipeListSerializer(serializers.ModelSerializer):
    """Список рецептов"""
    # category = serializers.SlugRelatedField(slug_field='name', read_only=True)
    # owner = serializers.CharField(source="owner.phone_number", read_only=True)

    class Meta:
        model = Recipe
        fields = '__all__'


class RecipeDetailSerializer(serializers.ModelSerializer):
    """Один рецепт"""
    owner = serializers.CharField(source="owner.phone_number", read_only=True)
    category = serializers.SlugRelatedField(slug_field='name', read_only=True)
    kitchen = serializers.SlugRelatedField(slug_field='name', read_only=True)
    ingredients = IngredientSerializer(many=True)
    tags = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True)
    comments = CommentSerializer(many=True)

    class Meta:
        model = Recipe
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    """Продукт"""
    class Meta:
        model = Product
        fields = "__all__"