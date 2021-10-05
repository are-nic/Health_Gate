from rest_framework import serializers
from .models import Order, OrderRecipe, OrderProduct


class OrderRecipeSerializer(serializers.ModelSerializer):
    """
    Рецепт заказа
    """
    class Meta:
        model = OrderRecipe
        fields = '__all__'


class OrderProductSerializer(serializers.ModelSerializer):
    """
    Продукт заказа
    """
    class Meta:
        model = OrderProduct
        fields = '__all__'


class OrderListSerializer(serializers.ModelSerializer):
    """Список Заказов"""
    class Meta:
        model = Order
        fields = '__all__'


class OrderDetailSerializer(serializers.ModelSerializer):
    """Один Заказ"""

    customer = serializers.CharField(source="customer.phone_number", read_only=True)
    recipes = OrderRecipeSerializer(many=True)
    products = OrderProductSerializer(many=True)

    class Meta:
        model = Order
        fields = '__all__'