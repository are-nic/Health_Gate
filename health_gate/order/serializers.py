from rest_framework import serializers
from .models import Order, OrderRecipe, OrderProduct


class OrderSerializer(serializers.ModelSerializer):
    """Заказы"""
    class Meta:
        model = Order
        fields = '__all__'


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