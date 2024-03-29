from rest_framework import serializers
from .models import Ingredient, Recipe, IngredientRecipe, Comment, Product, CookStep, Category, Kitchen, Tag, Subtype, Filter
from django.contrib.auth import get_user_model
from drf_extra_fields.fields import Base64ImageField
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


class IngredientRecipeSerializer(serializers.ModelSerializer):
    """
    Ингредиент
    """
    recipe = serializers.SlugRelatedField(slug_field='title', queryset=Recipe.objects.all())
    product = serializers.SlugRelatedField(slug_field='name', queryset=Product.objects.all())
    unit = serializers.ChoiceField(choices=IngredientRecipe.UNITS)

    class Meta:
        model = IngredientRecipe
        fields = ['id', 'recipe', 'product', 'qty', 'unit']


class IngredientProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name',  'picture', 'qty_per_item', 'price', 'shop_id']


class IngredientRecipeWithProductSerializer(serializers.ModelSerializer):
    product = IngredientProductSerializer()

    class Meta:
        model = IngredientRecipe
        fields = ['id',  'product', 'qty']


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

    class Meta:
        model = CookStep
        fields = '__all__'


class UserForRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'phone_number', 'full_name', 'profession', 'photo']


# ----------------------------------------------------Recipes Only-------------------------------------------------
class RecipeListSerializer(serializers.ModelSerializer):
    """Вывод списка рецептов"""
    owner = UserForRecipeSerializer()
    category = serializers.SlugRelatedField(slug_field='name', queryset=Category.objects.all())
    kitchen = serializers.SlugRelatedField(slug_field='name', queryset=Kitchen.objects.all())
    level = ChoiceField(choices=Recipe.LEVEL)
    tags = serializers.SlugRelatedField(many=True, slug_field='name', queryset=Tag.objects.all())

    class Meta:
        model = Recipe
        exclude = ['is_active', 'date_created']


class RecipeCreateSerializer(serializers.ModelSerializer):
    """Для создания рецепта"""
    owner = serializers.ReadOnlyField(source='owner.phone_number')
    category = serializers.SlugRelatedField(slug_field='name', queryset=Category.objects.all())
    kitchen = serializers.SlugRelatedField(slug_field='name', queryset=Kitchen.objects.all())
    level = ChoiceField(choices=Recipe.LEVEL)
    tags = serializers.SlugRelatedField(many=True, slug_field='name', queryset=Tag.objects.all())
    media = Base64ImageField()

    class Meta:
        model = Recipe
        exclude = ['is_active', 'date_created']


class RecipeDetailSerializer(serializers.ModelSerializer):
    """Вывод одного рецепта"""
    owner = UserForRecipeSerializer()
    category = serializers.SlugRelatedField(slug_field='name', queryset=Category.objects.all())
    kitchen = serializers.SlugRelatedField(slug_field='name', queryset=Kitchen.objects.all())
    ingredients = IngredientRecipeWithProductSerializer(many=True)
    level = ChoiceField(choices=Recipe.LEVEL)
    steps = CookStepSerializer(many=True)
    tags = serializers.SlugRelatedField(many=True, slug_field='name', queryset=Tag.objects.all())
    comments = CommentSerializer(many=True)

    class Meta:
        model = Recipe
        fields = '__all__'


class RecipeSerializer(serializers.ModelSerializer):
    """для обновления рецепта"""
    owner = serializers.ReadOnlyField(source='owner.phone_number')
    category = serializers.SlugRelatedField(slug_field='name', queryset=Category.objects.all())
    kitchen = serializers.SlugRelatedField(slug_field='name', queryset=Kitchen.objects.all())
    ingredients = IngredientRecipeSerializer(many=True)
    level = ChoiceField(choices=Recipe.LEVEL)
    steps = CookStepSerializer(many=True, required=False)
    tags = serializers.SlugRelatedField(many=True, slug_field='name', queryset=Tag.objects.all())
    comments = CommentSerializer(many=True, required=False)

    class Meta:
        model = Recipe
        fields = '__all__'

    def update(self, instance, validated_data):
        """
        Обновление экземпляра рецепта с ингредиентами и тегами
        """
        if 'ingredients' in validated_data:
            ingredients_data = validated_data.pop('ingredients')
            ingredients = instance.ingredients.all()
            ingredients = list(ingredients)
            for ingredient_data in ingredients_data:
                ingredient = ingredients.pop(0)
                ingredient.product = ingredient_data.get('product', ingredient.product)
                ingredient.qty = ingredient_data.get('qty', ingredient.qty)
                ingredient.unit = ingredient_data.get('unit', ingredient.unit)
                ingredient.save()

        if 'steps' in validated_data:
            steps_data = validated_data.pop('steps')
            steps = instance.steps.all()
            steps = list(steps)
            for step_data in steps_data:
                step = steps.pop(0)
                step.title = step_data.get('title', step.title)
                step.description = step_data.get('description', step.description)
                step.image = step_data.get('image', step.image)
                step.save()

        instance.category = validated_data.get('category', instance.category)
        instance.kitchen = validated_data.get('kitchen', instance.kitchen)
        instance.title = validated_data.get('title', instance.title)
        instance.slug = validated_data.get('slug', instance.slug)
        instance.level = validated_data.get('level', instance.level)
        instance.no_preservatives = validated_data.get('no_preservatives', instance.no_preservatives)
        instance.cooking_time = validated_data.get('cooking_time', instance.cooking_time)
        instance.protein = validated_data.get('protein', instance.protein)
        instance.fat = validated_data.get('fat', instance.fat)
        instance.carbohydrates = validated_data.get('carbohydrates', instance.carbohydrates)
        instance.kkal = validated_data.get('kkal', instance.kkal)
        instance.description = validated_data.get('description', instance.description)
        instance.media = validated_data.get('media', instance.media)
        instance.price = validated_data.get('price', instance.price)
        instance.portions = validated_data.get('portions', instance.portions)
        instance.date_created = validated_data.get('date_created', instance.date_created)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        if 'tags' in validated_data:
            tags_data = validated_data.pop('tags')
            for tag_data in tags_data:
                tag = Tag.objects.get(name=tag_data)
                instance.tags.add(tag)
        instance.save()

        return instance
# --------------------------------------------------------------------------------------------------------------------


class ProductSerializer(serializers.ModelSerializer):
    """Продукт"""
    class Meta:
        model = Product
        fields = "__all__"


class TagSerializer(serializers.ModelSerializer):
    """Тэги"""

    class Meta:
        model = Tag
        fields = ('name',)


class SubtypeSerializer(serializers.ModelSerializer):
    """Подтипы тегов"""

    tags = TagSerializer(many=True)

    class Meta:
        model = Subtype
        fields = ('title', 'icon', 'tags')


class FilterSerializer(serializers.ModelSerializer):
    """Основные фильтры"""
    subtypes = SubtypeSerializer(many=True, read_only=True)

    class Meta:
        model = Filter
        fields = ('title', 'subtypes')


class RecipeCategorySerializer(serializers.ModelSerializer):
    """Категории рецептов"""

    class Meta:
        model = Category
        exclude = ('slug',)


class KitchenSerializer(serializers.ModelSerializer):
    """Кухня"""

    class Meta:
        model = Kitchen
        exclude = ('slug',)


class IngredientsListSerializer(serializers.ModelSerializer):
    """Вывод списка ингредиентов"""

    class Meta:
        model = Ingredient
        exclude = ['id']