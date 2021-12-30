from rest_framework import serializers
from food.models import Recipe, Product
from .models import Order, OrderRecipe, MealPlanRecipe
from food.serializers import ChoiceField


'''
class OrderProductSerializer(serializers.ModelSerializer):
    """
    Продукт заказа
    """
    product = serializers.SlugRelatedField(slug_field='name', queryset=Product.objects.all())
    # для переименования поля recipe в ответе
    order_recipe = serializers.PrimaryKeyRelatedField(source='recipe', queryset=OrderRecipe.objects.all())

    class Meta:
        model = OrderProduct
        exclude = ['recipe']
        # fields = '__all__'
'''


class OrderRecipeSerializer(serializers.ModelSerializer):
    """
    Рецепт заказа
    """
    recipe = serializers.SlugRelatedField(slug_field='title', queryset=Recipe.objects.all())

    class Meta:
        model = OrderRecipe
        fields = ('recipe', 'qty')


'''
class OrderRecipeDetailSerializer(serializers.ModelSerializer):
    """
    Рецепт заказа
    """
    products = OrderProductSerializer(many=True)
    recipe = serializers.SlugRelatedField(slug_field='title', queryset=Recipe.objects.all())

    class Meta:
        model = OrderRecipe
        fields = '__all__'
'''


class OrderListSerializer(serializers.ModelSerializer):
    """Список Заказов"""
    customer = serializers.CharField(source="customer.phone_number", read_only=True)
    pay_method = ChoiceField(choices=Order.PAY_METHOD)

    class Meta:
        model = Order
        fields = '__all__'


class OrderDetailSerializer(serializers.ModelSerializer):
    """Один Заказ"""

    customer = serializers.CharField(source="customer.phone_number", read_only=True)
    recipes = OrderRecipeSerializer(many=True)
    pay_method = ChoiceField(choices=Order.PAY_METHOD)

    class Meta:
        model = Order
        fields = '__all__'

    def update(self, instance, validated_data):
        """
        Обновление экземпляра рецепта заказа и самого заказа
        """
        if 'recipes' in validated_data:
            recipes_data = validated_data.pop('recipes')
            recipes = instance.recipes.all()
            recipes = list(recipes)
            for recipe_data in recipes_data:
                recipe = recipes.pop(0)
                recipe.qty = recipe_data.get('qty', recipe.qty)
                recipe.save()

        instance.name = validated_data.get('name', instance.name)
        instance.address = validated_data.get('address', instance.address)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.pay_method = validated_data.get('pay_method', instance.pay_method)
        instance.at_door = validated_data.get('at_door', instance.at_door)
        instance.promocode = validated_data.get('promocode', instance.promocode)
        instance.save()

        return instance


class MealPlanRecipeSerializer(serializers.ModelSerializer):
    """Рецепт плана питания"""

    owner = serializers.CharField(source='owner.phone_number', read_only=True)
    recipe = serializers.SlugRelatedField(slug_field='title', queryset=Recipe.objects.all())

    class Meta:
        model = MealPlanRecipe
        fields = '__all__'
