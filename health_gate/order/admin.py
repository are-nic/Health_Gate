from django.contrib import admin
from .models import *


class OrderRecipeInline(admin.TabularInline):
    model = OrderRecipe
    raw_id_fields = ['recipe']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'created_at', 'updated_at', 'paid']
    inlines = [OrderRecipeInline, ]