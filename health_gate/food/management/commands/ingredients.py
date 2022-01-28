# Добавление ингредиентов в БД из файла "export_tovar_tag.csv"
# Для запуска - python manage.py ingredients

import csv
from ...models import Ingredient
from django.core.management import BaseCommand


def get_ingredients():
    """
    В файле нет имен колонок, поэтому присваиваем имя колонке с ингредиентами - fieldnames=['ingredient']
    Ингредиенты из файла добавляются во множество ingredients для исключения повторений.
    В результате создается множество объектов Ингредиентов
    """
    ingredients = set()
    with open(r'D:\downloads\telegram\БД ингредиенты 20.12.21\export_tovar_tag.csv', encoding='utf-8') as file:
        data = csv.DictReader(file, fieldnames=['ingredient'])
        for row in data:
            if row not in ['удалить', '']:
                ingredients.add(row['ingredient'])
    objs = [Ingredient(name=name) for name in ingredients]
    Ingredient.objects.bulk_create(objs)


class Command(BaseCommand):
    def handle(self, *args, **options):
        get_ingredients()
        print("Ингредиенты занесены в БД")