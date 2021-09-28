from decimal import Decimal
from django.core.validators import MinValueValidator
from django.db import models
from slugify import slugify
from django.contrib.auth import get_user_model

User = get_user_model()


class Category(models.Model):
    """
    категории рецептов
    """
    name = models.CharField(max_length=100, verbose_name="Название категории")
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        db_table = 'category_recipe'

    def __str__(self):
        return self.name


class Kitchen(models.Model):
    """
    Типы кухонь (азиатская, европейская и т.д.)
    """
    name = models.CharField(max_length=100, verbose_name="Тип кухни")
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Кухня'
        verbose_name_plural = 'Кухни'
        db_table = 'kitchen'

    def __str__(self):
        return self.name


class Tag(models.Model):
    """
    Тэги
    """
    name = models.CharField(max_length=100, verbose_name='Тэг')

    class Meta:
        ordering = ('name',)
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'
        db_table = 'tags'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """
    Рецепт
    """
    LEVEL = [
        ('HARD', 'сложно'),
        ('MIDDLE', 'средне'),
        ('EASY', 'легко'),
    ]

    LIVE_STYLE = []
    HEALTH_STATUS = []
    DIET = []

    owner = models.ForeignKey(User, verbose_name='Автор рецепта', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.SET_NULL, null=True, blank=True)
    kitchen = models.ForeignKey(Kitchen, verbose_name='Тип кухни', on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=255, verbose_name='Название рецепта')
    slug = models.SlugField(unique=True)
    level = models.CharField(max_length=20, choices=LEVEL, verbose_name='Уровень сложности блюда')
    no_preservatives = models.BooleanField(default=False, verbose_name='Без консервантов')
    live_style = models.CharField(max_length=30, choices=LIVE_STYLE, verbose_name='Стиль жизни')
    health_status = models.CharField(max_length=30, choices=HEALTH_STATUS, verbose_name='Состояние здоровья')
    diet = models.CharField(max_length=30, choices=DIET, verbose_name='Тип диеты')
    cooking_time = models.CharField(max_length=50, verbose_name='Время приготовления')
    protein = models.IntegerField(verbose_name='Белки', null=True)
    fat = models.IntegerField(verbose_name='Жиры', null=True)
    carbohydrates = models.IntegerField(verbose_name='Углеводы', null=True)
    kkal = models.IntegerField(verbose_name='Калории', null=True)
    description = models.TextField(verbose_name='Описание')
    image = models.ImageField(verbose_name='Фото блюда', blank=True, null=True, upload_to='recipes')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена',
                                default=0.00, validators=[MinValueValidator(Decimal('0.00'))])
    portions = models.PositiveIntegerField(verbose_name='Кол-во порций', default=1)
    date_created = models.DateTimeField(auto_now_add=True, null=True, verbose_name='создан')
    tags = models.ManyToManyField(Tag, blank=True, default='рецепт', verbose_name='Тэги')

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        db_table = 'Recipe'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """
        для автоматического заполнения поля slug при создании рецепта
        """
        self.slug = slugify(str(self.title))
        return super(Recipe, self).save(*args, **kwargs)

    @property
    def imageURL(self):
        """метод для использования в шаблонах ссылки на изображение рецепта"""
        try:
            url = self.image.url
        except:
            url = ''
        return url


class Ingredient(models.Model):
    """
    экземпляр ингридиента, который принадлежит к конкретному рецепту в определенном кол-ве.
    для получения всех ингридиентов по какому либо рецепту использовать: recipe.ingredients.all()
    """

    UNITS = [
        ('LITER', 'л.'),
        ('MILLI', 'мл.'),
        ('GRAMM', 'г.'),
        ('KILO', 'кг.'),
        ('PIECES', 'шт.'),
        ('TASTE', 'по вкусу'),
        ('TEA SPOON', 'ч. ложка'),
        ('TABLESPOON', 'ст. ложка'),
        ('GLASS', 'стакан'),
    ]

    recipe = models.ForeignKey(Recipe, verbose_name='Рецепт', on_delete=models.CASCADE, related_name='ingredients')
    id_product = models.PositiveIntegerField(verbose_name='id продукта', null=True, blank=True)
    name = models.CharField(max_length=200, verbose_name='Имя ингредиента')
    qty = models.PositiveIntegerField(verbose_name='Кол-во')
    unit = models.CharField(max_length=20, choices=UNITS, verbose_name='Ед. измерения')

    class Meta:
        ordering = ('name',)
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        db_table = 'Ingredient'

    def __str__(self):
        return self.name.name


class CookStep(models.Model):
    """
    Модель шага приготовления рецепта
    У каждого рецепта есть шаги по приготовлению оного.
    """
    recipe = models.ForeignKey(Recipe, verbose_name='Рецепт', on_delete=models.CASCADE, related_name='steps')
    title = models.CharField(max_length=200, verbose_name='Заголовок шага')
    description = models.TextField(verbose_name='Описание шага')
    image = models.ImageField(verbose_name='Фото шага', blank=True, null=True, upload_to='steps') # прописать грамотно путь