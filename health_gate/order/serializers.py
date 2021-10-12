from rest_framework import serializers
from food.models import Recipe
from .models import Order, OrderRecipe, OrderProduct, MealPlanRecipe
from food.serializers import ChoiceField


class OrderProductSerializer(serializers.ModelSerializer):
    """
    Продукт заказа
    """
    recipe = serializers.SlugRelatedField(slug_field='title', queryset=Recipe.objects.all())

    class Meta:
        model = OrderProduct
        fields = '__all__'


class OrderRecipeSerializer(serializers.ModelSerializer):
    """
    Рецепт заказа
    """
    # products = OrderProductSerializer(many=True)
    recipe = serializers.SlugRelatedField(slug_field='title', queryset=Recipe.objects.all())

    class Meta:
        model = OrderRecipe
        exclude = ['order']


class OrderSerializer(serializers.ModelSerializer):
    """Заказ"""

    customer = serializers.CharField(source="customer.phone_number", read_only=True)
    recipes = OrderRecipeSerializer(many=True)
    pay_method = ChoiceField(choices=Order.PAY_METHOD)

    class Meta:
        model = Order
        fields = '__all__'


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


class MealPlanRecipeSerializer(serializers.ModelSerializer):
    """Рецепт плана питания"""

    owner = serializers.ReadOnlyField(source='owner.phone_number')
    recipe = serializers.SlugRelatedField(slug_field='name', queryset=Recipe.objects.all())

    class Meta:
        model = MealPlanRecipe
        fields = '__all__'

    def validate_recipe(self, value):
        if value.user != self.context['request'].user:
            raise serializers.ValidationError('Неверный id рецепта')
        return value