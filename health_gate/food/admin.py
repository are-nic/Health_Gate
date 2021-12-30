from django.contrib import admin
from .models import *


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}   # для автозаполнения поля slug у модели Category


@admin.register(Kitchen)
class KitchenAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}   # для автозаполнения поля slug у модели Kitchen


class IngredientRecipeAdmin(admin.TabularInline):     # для вложенных в экземпляр рецепта ингредиентов
    model = IngredientRecipe


class CookStepAdmin(admin.TabularInline):       # для вложенных в экземпляр рецепта шагов приготолвения
    model = CookStep


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    # prepopulated_fields = {'slug': ('title',)}  # для автозаполнения поля slug у модели Recipe
    filter_horizontal = ('tags',)               # выбор тэгов
    inlines = [IngredientRecipeAdmin, CookStepAdmin]


admin.site.register(Tag)
admin.site.register(Subtype)
admin.site.register(Filter)
admin.site.register(Comment)
admin.site.register(Product)
admin.site.register(CategoryProduct)
admin.site.register(Ingredient)