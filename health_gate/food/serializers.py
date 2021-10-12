from rest_framework import serializers
from .models import Recipe, Ingredient, Comment, Product, CookStep, Category, Kitchen, Tag
from django.contrib.auth import get_user_model

User = get_user_model()


class ChoiceField(serializers.ChoiceField):
    """
    Настраиваемое поле для поля выбора значений
    """
    def to_representation(self, obj):
        # Предоставляет читабельное значение из списка choices полей модели
        if obj == '' and self.allow_blank:
            return obj
        return self._choices[obj]

    def to_internal_value(self, data):
        # Поддерживает отправляемые значения через post, put, patch методы
        if data == '' and self.allow_blank:
            return ''

        for key, val in self._choices.items():
            if val == data:
                return key
        self.fail('invalid_choice', input=data)


class IngredientSerializer(serializers.ModelSerializer):
    """
    Ингредиент
    """
    recipe = serializers.SlugRelatedField(slug_field='title', queryset=Recipe.objects.all())
    unit = serializers.ChoiceField(choices=Ingredient.UNITS)

    class Meta:
        model = Ingredient
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    """
    Комментария к рецепту
    """
    author = serializers.ReadOnlyField(source='author.phone_number')
    recipe = serializers.SlugRelatedField(slug_field='title', queryset=Recipe.objects.all())

    class Meta:
        model = Comment
        fields = '__all__'


class CookStepSerializer(serializers.ModelSerializer):
    """
    Шаги приготовления рецепт
    """
    recipe = serializers.SlugRelatedField(slug_field='title', queryset=Recipe.objects.all())

    class Meta:
        model = CookStep
        fields = '__all__'


class RecipeListSerializer(serializers.ModelSerializer):
    """Список рецептов"""
    owner = serializers.ReadOnlyField(source='owner.phone_number')
    level = ChoiceField(choices=Recipe.LEVEL)
    category = serializers.SlugRelatedField(slug_field='name', queryset=Category.objects.all())
    kitchen = serializers.SlugRelatedField(slug_field='name', queryset=Kitchen.objects.all())
    tags = serializers.SlugRelatedField(many=True, slug_field='name', queryset=Tag.objects.all())

    class Meta:
        model = Recipe
        fields = '__all__'


class RecipeDetailSerializer(serializers.ModelSerializer):
    """Один рецепт"""
    owner = serializers.ReadOnlyField(source='owner.phone_number')
    category = serializers.SlugRelatedField(slug_field='name', queryset=Category.objects.all())
    kitchen = serializers.SlugRelatedField(slug_field='name', queryset=Kitchen.objects.all())
    ingredients = IngredientSerializer(many=True, required=False)
    level = ChoiceField(choices=Recipe.LEVEL)
    steps = CookStepSerializer(many=True, required=False)
    tags = serializers.SlugRelatedField(many=True, slug_field='name', queryset=Tag.objects.all())
    comments = CommentSerializer(many=True, required=False)

    class Meta:
        model = Recipe
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    """Продукт"""
    class Meta:
        model = Product
        fields = "__all__"