from rest_framework import serializers
from food.models import Recipe, Product
from .models import Order, OrderRecipe, OrderProduct, MealPlanRecipe
from food.serializers import ChoiceField


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


class OrderRecipeSerializer(serializers.ModelSerializer):
    """
    Рецепт заказа
    """
    # products = OrderProductSerializer(many=True)
    recipe = serializers.SlugRelatedField(slug_field='title', queryset=Recipe.objects.all())

    class Meta:
        model = OrderRecipe
        fields = '__all__'


class OrderRecipeDetailSerializer(serializers.ModelSerializer):
    """
    Рецепт заказа
    """
    products = OrderProductSerializer(many=True)
    recipe = serializers.SlugRelatedField(slug_field='title', queryset=Recipe.objects.all())

    class Meta:
        model = OrderRecipe
        fields = '__all__'


# -----------------------------------------------------For Nested Routers-----------------------------------------
class OrderSerializer(serializers.ModelSerializer):
    """Заказ"""

    customer = serializers.CharField(source="customer.phone_number", read_only=True)
    recipes = OrderRecipeSerializer(many=True)
    pay_method = ChoiceField(choices=Order.PAY_METHOD)

    class Meta:
        model = Order
        fields = '__all__'
# ------------------------------------------------------------------------------------------------------------


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

    owner = serializers.CharField(source='owner.phone_number', read_only=True)
    recipe = serializers.SlugRelatedField(slug_field='title', queryset=Recipe.objects.all())

    class Meta:
        model = MealPlanRecipe
        fields = '__all__'