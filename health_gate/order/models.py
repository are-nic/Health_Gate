from django.conf import settings
from django.db import models
from food.models import Recipe, Product


User = settings.AUTH_USER_MODEL


class Order(models.Model):
    """
    Модель Заказа
    """
    PAY_METHOD = [
        ('UPON_RECEIPT', 'Оплатить наличными или картой при получении'),
        ('ONLINE', 'Оплатить онлайн'),
    ]
    customer = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Покупатель', null=True)
    name = models.CharField(max_length=50, verbose_name='Имя', blank=True, null=True)
    address = models.CharField(max_length=250, verbose_name='Адрес доставки', null=True)
    phone_number = models.PositiveIntegerField(verbose_name='Телефон', blank=True, null=True)
    pay_method = models.CharField(max_length=12, choices=PAY_METHOD, verbose_name='Способ оплаты')
    at_door = models.BooleanField(default=False, verbose_name='Оставить заказ у дверей')
    promocode = models.CharField(max_length=50, verbose_name='Промокод', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Изменен')
    paid = models.BooleanField(default=False, verbose_name='Оплачен')

    class Meta:
        ordering = ('updated_at',)
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        db_table = 'order'

    def __str__(self):
        return self.customer.phone_number


class OrderRecipe(models.Model):
    """
    Модель Рецепта в заказе
    """
    order = models.ForeignKey(Order, related_name='recipes', on_delete=models.CASCADE, verbose_name='Заказ')
    recipe = models.ForeignKey(Recipe, related_name='recipes', on_delete=models.CASCADE, verbose_name='Рецепт')
    qty = models.PositiveIntegerField(verbose_name='Кол-во порций')

    class Meta:
        ordering = ('order',)
        verbose_name = 'Рецепт заказа'
        verbose_name_plural = 'Рецепты заказа'
        db_table = 'order_recipe'

    def __str__(self):
        return self.recipe.title


'''class OrderProduct(models.Model):
    """
    Модель Продукта в заказе
    """
    order = models.ForeignKey(Order, related_name='products', on_delete=models.CASCADE, verbose_name='Заказ')
    recipe = models.ForeignKey(OrderRecipe, related_name='products', on_delete=models.CASCADE, verbose_name='Рецепт заказа')
    product = models.ForeignKey(Product, related_name='order_product', on_delete=models.CASCADE, verbose_name='Продукт')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    qty = models.PositiveIntegerField(verbose_name='Кол-во единиц')
    delivery_datetime = models.DateTimeField(verbose_name='Дата и время доставки', default=None)

    class Meta:
        ordering = ('recipe',)
        verbose_name = 'Продукт заказа'
        verbose_name_plural = 'Продукты заказа'
        db_table = 'order_product'

    def __str__(self):
        return self.product.name'''


class MealPlanRecipe(models.Model):
    """
    Рецепт плана питания
    """
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Владелец плана', related_name='plan')
    recipe = models.ForeignKey(Recipe, related_name='recipe_plan', on_delete=models.CASCADE, verbose_name='Рецепт')
    qty = models.PositiveIntegerField(verbose_name='Кол-во порций')
    date = models.DateField(verbose_name='Плановая дата')

    class Meta:
        ordering = ('owner',)
        verbose_name = 'Рецепт плана питания'
        verbose_name_plural = 'Рецепты плана питания'
        db_table = 'meal_plan_recipes'

    def __str__(self):
        return self.recipe.title