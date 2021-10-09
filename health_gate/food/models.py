from decimal import Decimal

from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from slugify import slugify


User = settings.AUTH_USER_MODEL


class Product(models.Model):
    """Продукт"""

    CATEGORIES = [
        ('MILK', 'Молочка'),
        ('MEAT', 'Мясо'),
        ('BREAD', 'Хлебные изделия'),
        ('FRUIT', 'Фрукты'),
        ('VEGETABLES', 'Овощи')
    ]

    UNITS = [
        ('LITER', 'л.'),
        ('MILLI', 'мл.'),
        ('GRAM', 'г.'),
        ('KILO', 'кг.'),
        ('PIECES', 'шт.')
    ]

    category = models.CharField(max_length=10, choices=CATEGORIES, verbose_name='Категория', null=True, blank=True)
    name = models.CharField(max_length=300, verbose_name='Наименование')
    qty_per_item = models.PositiveIntegerField(verbose_name='Кол-во на ед. продукта', null=True, blank=True)
    unit = models.CharField(max_length=10, choices=UNITS, verbose_name='Ед. измерения', null=True, blank=True)
    # image = models.ImageField(upload_to='recipes/%Y/%m/%d', blank=True, verbose_name='Фото')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена', default=0.00)
    stock = models.PositiveIntegerField(verbose_name='Остаток ед. продукта', default=1)
    available = models.BooleanField(default=True, verbose_name='В наличии')
    added = models.DateTimeField(auto_now_add=True, verbose_name='Добавлен')
    updated = models.DateTimeField(auto_now=True, verbose_name='Обновлен')

    class Meta:
        ordering = ('name',)
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        db_table = 'product'

    def __str__(self):
        return self.name


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


class Filter(models.Model):
    """
    Модель основных фильтров предпочтений (тегов) (в соответствии с дизайном: Стиль жизни, Состояние здоровья, Диета)
    """
    title = models.CharField(max_length=100, verbose_name='Заголовок фильтра')

    class Meta:
        ordering = ('title',)
        verbose_name = 'Фильтр'
        verbose_name_plural = 'Фильтры'
        db_table = 'filter'

    def __str__(self):
        return self.title


class Subtype(models.Model):
    """
    Модель подтипов предпочтений (тегов) (в соответствии с дизайном: Короновирус, Старение, Здоровье мозга и т.д.)
    """
    filter = models.ForeignKey(Filter, verbose_name='Основные фильтры предпочтений', on_delete=models.CASCADE)
    title = models.CharField(max_length=100, verbose_name='Заголовок подтипа')

    class Meta:
        ordering = ('title',)
        verbose_name = 'Подтип'
        verbose_name_plural = 'Подтипы'
        db_table = 'subtype'

    def __str__(self):
        return self.title


class Tag(models.Model):
    """
    Тэги
    """
    subtype = models.ForeignKey(Subtype, verbose_name='Подтип предпочтений/тегов', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name='Тэг', unique=True)

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

    owner = models.ForeignKey(User, verbose_name='Автор рецепта', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.SET_NULL, null=True, blank=True)
    kitchen = models.ForeignKey(Kitchen, verbose_name='Тип кухни', on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=255, verbose_name='Название рецепта')
    slug = models.SlugField(unique=True)
    level = models.CharField(max_length=20, choices=LEVEL, verbose_name='Уровень сложности блюда')
    no_preservatives = models.BooleanField(default=False, verbose_name='Без консервантов')
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
    tags = models.ManyToManyField(Tag, blank=True, verbose_name='Тэги')
    is_active = models.BooleanField(default=False, verbose_name='Прошел модерацию')

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
        self.slug = slugify(self.title)
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
        ('GRAM', 'г.'),
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
        return self.name


class CookStep(models.Model):
    """
    Модель шага приготовления рецепта
    У каждого рецепта есть шаги по приготовлению оного.
    """
    recipe = models.ForeignKey(Recipe, verbose_name='Рецепт', on_delete=models.CASCADE, related_name='steps')
    title = models.CharField(max_length=200, verbose_name='Заголовок шага')
    description = models.TextField(verbose_name='Описание шага')
    image = models.ImageField(verbose_name='Фото шага', blank=True, null=True, upload_to='steps')   # указать путь

    class Meta:
        ordering = ('title',)
        verbose_name = 'Шаг приготовления'
        verbose_name_plural = 'Шаги приготовления'
        db_table = 'cook_steps'

    def __str__(self):
        return self.title


class Comment(models.Model):
    """
    Комментарий к рецепту
    """
    author = models.ForeignKey(User, verbose_name='Автор комментария', on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, verbose_name='Рецепт', on_delete=models.CASCADE, related_name='comments')
    text = models.TextField(verbose_name='Текст комментария')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создан')

    class Meta:
        ordering = ('recipe',)
        verbose_name = 'Комментарий к рецепту'
        verbose_name_plural = 'Комментарии к рецепту'
        db_table = 'comments_recipe'

    def __str__(self):
        return self.recipe.title