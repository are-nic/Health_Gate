from django.db import models
from food.models import Recipe, Product
from django.contrib.auth import get_user_model


User = get_user_model()


class Order(models.Model):
    """
    Модель Заказа
    """
    PAY_METHOD = [
        ('UPON_RECEIPT', 'Оплатить наличными или картой при получении'),
        ('ONLINE', 'Оплатить онлайн'),
    ]
    customer = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, verbose_name='Покупатель')
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
        return 'Заказ от: {}'.format(self.customer.phone_number)


class OrderRecipe(models.Model):
    """
    Модель Рецепта в заказе
    """
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE, verbose_name='Заказ')
    recipe = models.ForeignKey(Recipe, related_name='recipe_items', on_delete=models.CASCADE, verbose_name='Рецепт')
    qty = models.PositiveIntegerField(verbose_name='Кол-во порций')

    class Meta:
        ordering = ('order',)
        verbose_name = 'Рецепт заказа'
        verbose_name_plural = 'Рецепты заказа'
        db_table = 'order_recipe'

    def __str__(self):
        return '{}'.format(self.recipe)


class OrderProduct(models.Model):
    """
    Модель Продукта в заказе
    """
    order = models.ForeignKey(Order, related_name='item', on_delete=models.CASCADE, verbose_name='Заказ')
    recipe = models.ForeignKey(Recipe, related_name='recipe_item', on_delete=models.CASCADE, verbose_name='Рецепт')
    product = models.ForeignKey(Product, related_name='product_item', on_delete=models.CASCADE, verbose_name='Продукт')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    qty = models.PositiveIntegerField(verbose_name='Кол-во единиц')
    delivery_datetime = models.DateTimeField(verbose_name='Дата и время доставки', default=None)

    class Meta:
        ordering = ('recipe',)
        verbose_name = 'Продукт заказа'
        verbose_name_plural = 'Продукты заказа'
        db_table = 'order_product'

    def __str__(self):
        return '{}'.format(self.product)