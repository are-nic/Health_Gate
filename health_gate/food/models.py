from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL


class Ingredient(models.Model):
    """
    Ингредиент
    """
    name = models.CharField(max_length=100, verbose_name='Название')

    class Meta:
        ordering = ('name',)
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        db_table = 'Ingredients'

    def __str__(self):
        return self.name


class CategoryProduct(models.Model):
    """Категории продуктов"""

    shop = models.CharField(max_length=50, verbose_name='Магазин', null=True, blank=True)
    name = models.CharField(max_length=50, verbose_name="Название категории")

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория продукта'
        verbose_name_plural = 'Категории продуктов'
        db_table = 'category_product'

    def __str__(self):
        return self.name


class Product(models.Model):
    """Продукт"""

    UNITS = [
        ('л', 'л'),
        ('мл', 'мл'),
        ('г', 'г'),
        ('кг', 'кг'),
        ('шт', 'шт')
    ]

    ingredient = models.ForeignKey(Ingredient, verbose_name='Ингредиент', on_delete=models.CASCADE,
                                   related_name='products')
    shop = models.CharField(max_length=50, verbose_name='Магазин', null=True, blank=True)
    category = models.ForeignKey(CategoryProduct, verbose_name='Категория', on_delete=models.CASCADE,
                                 db_constraint=False, null=True, blank=True)
    shop_id = models.PositiveIntegerField(verbose_name='ID продукта в магазине', null=True, blank=True)
    name = models.CharField(max_length=300, verbose_name='Наименование')
    qty_per_item = models.FloatField(verbose_name='Кол-во на ед. продукта', null=True, blank=True)
    unit = models.CharField(max_length=10, choices=UNITS, verbose_name='Ед. измерения', null=True, blank=True)
    # image = models.ImageField(upload_to='products', verbose_name='Фото', null=True, blank=True)
    picture = models.URLField(verbose_name='Фото', null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена', default=0.00)
    proteins = models.FloatField(verbose_name='Белки', null=True, blank=True)
    fats = models.FloatField(verbose_name='Жиры', null=True, blank=True)
    carbohydrates = models.FloatField(verbose_name='Углеводы', null=True, blank=True)
    calories = models.FloatField(verbose_name='Калории', null=True, blank=True)
    available = models.BooleanField(default=True, verbose_name='В наличии')
    added = models.DateTimeField(auto_now_add=True, verbose_name='Добавлен')
    updated = models.DateTimeField(auto_now=True, verbose_name='Обновлен')
    analogs = models.ManyToManyField('food.Product', related_name='analog_products')

    class Meta:
        ordering = ('name',)
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        db_table = 'product'

    def __str__(self):
        return self.name


class Category(models.Model):
    """
    Категории рецептов
    """
    name = models.CharField(max_length=100, verbose_name="Название категории")
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория рецептов'
        verbose_name_plural = 'Категории рецептов'
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
    filter = models.ForeignKey(Filter, verbose_name='Основные фильтры предпочтений', on_delete=models.CASCADE,
                               related_name='subtypes')
    title = models.CharField(max_length=100, verbose_name='Заголовок подтипа')
    icon = models.FileField(verbose_name='Иконка подтипа', upload_to='tags', blank=True, null=True)

    class Meta:
        ordering = ('title',)
        verbose_name = 'Подтип'
        verbose_name_plural = 'Подтипы'
        db_table = 'subtype'

    def __str__(self):
        return self.title


class Tag(models.Model):
    """
    Теги
    """
    subtype = models.ForeignKey(Subtype, verbose_name='Подтип предпочтений/тегов', on_delete=models.CASCADE,
                                related_name='tags')
    name = models.CharField(max_length=100, verbose_name='Тэг', unique=True)

    class Meta:
        ordering = ('subtype',)
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

    EXTENSION = [
        ('PHOTO', 'photo'),
        ('VIDEO', 'video')
    ]

    owner = models.ForeignKey(User, verbose_name='Автор рецепта', on_delete=models.CASCADE, related_name='recipes')
    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.SET_NULL, null=True, blank=True)
    kitchen = models.ForeignKey(Kitchen, verbose_name='Тип кухни', on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=255, verbose_name='Название рецепта')
    level = models.CharField(max_length=20, choices=LEVEL, verbose_name='Уровень сложности блюда')
    no_preservatives = models.BooleanField(default=False, verbose_name='Без консервантов')
    cooking_time = models.CharField(max_length=50, verbose_name='Время приготовления')
    protein = models.IntegerField(verbose_name='Белки', null=True)
    fat = models.IntegerField(verbose_name='Жиры', null=True)
    carbohydrates = models.IntegerField(verbose_name='Углеводы', null=True)
    kkal = models.IntegerField(verbose_name='Калории', null=True)
    description = models.TextField(verbose_name='Описание')
    media = models.FileField(verbose_name='Фото/Видео', upload_to='recipes', blank=True, null=True)
    media_extension = models.CharField(max_length=5, choices=EXTENSION, verbose_name='Расширение файла media', null=True)
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


class IngredientRecipe(models.Model):
    """
    Ингредиент рецепта, который принадлежит к конкретному рецепту в определенном кол-ве.
    Так же имеет отношение к общему ингредиенту.
    Для получения всех ингредиентов по какому-либо рецепту использовать: recipe.ingredients.all()
    """

    UNITS = [
        ('л', 'л'),
        ('мл', 'мл'),
        ('г', 'г'),
        ('кг', 'кг'),
        ('шт', 'шт'),
        ('по вкусу', 'по вкусу'),
        ('ч. ложка', 'ч. ложка'),
        ('ст. ложка', 'ст. ложка'),
        ('стакан', 'стакан'),
    ]

    recipe = models.ForeignKey(Recipe, verbose_name='Рецепт', on_delete=models.CASCADE, related_name='ingredients')
    ingredient = models.ForeignKey(Ingredient, verbose_name='Ингредиент', on_delete=models.SET_NULL, null=True)
    qty = models.PositiveIntegerField(verbose_name='Кол-во')
    unit = models.CharField(max_length=20, choices=UNITS, verbose_name='Ед. измерения')

    class Meta:
        ordering = ('recipe',)
        verbose_name = 'Ингредиент рецепта'
        verbose_name_plural = 'Ингредиенты рецепта'
        db_table = 'IngredientRecipe'

    def __str__(self):
        return self.ingredient.name


class CookStep(models.Model):
    """
    Модель шага приготовления рецепта
    У каждого рецепта есть шаги по приготовлению оного.
    """
    recipe = models.ForeignKey(Recipe, verbose_name='Рецепт', on_delete=models.CASCADE, related_name='steps')
    ingredients = models.ManyToManyField(Product, verbose_name='Ингредиент', blank=True)
    title = models.CharField(max_length=200, verbose_name='Заголовок шага')
    description = models.TextField(verbose_name='Описание шага')
    image = models.ImageField(verbose_name='Фото шага', blank=True, null=True, upload_to='steps')

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
    author = models.ForeignKey(User, verbose_name='Автор комментария', on_delete=models.CASCADE, null=True)
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
