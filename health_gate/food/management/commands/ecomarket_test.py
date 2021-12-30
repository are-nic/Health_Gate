"""
Парсер тестовых данных по продуктам из Экомаркета
Для запуска обновления продуктов в БД из "EcoMarket" - python manage.py ecomarket_test
Для автообновления БД на сервере используется Corn, который через заданные промежутки времени запускает скрипт
"""

from ...models import CategoryProduct, Product
from django.core.management.base import BaseCommand
import xmltodict
import json
import requests
import re


def get_measure(name):
    """
    Метод нахождения меры веса/объема товара
    """
    pattern = r"[0-9]*[.,]?[0-9]{1,3}[ ]?(?:кг|гр|г|л|мл|шт)"
    if len(re.findall(pattern, name)) == 1:      # если кол-во найденых мер веса и объема в имени одного товара = 1
        qty_product = re.search(pattern, name)   # находим кол-во товара и его меру веса/объема

        measure_pattern = r"(?:кг|гр|г|л|мл|шт)\b"              # паттерн для поиска меры веса/объема
        measure = re.search(measure_pattern, qty_product[0])    # объект match найденой меры веса/объема

        if measure[0] == 'л' or measure[0] == 'мл':
            return 'мл'
        else:
            return 'г'


def get_organic(organic):
    """
    Метод обработки значений белков, жиров, углеводов из данных "EcoMarket" по каждому продукту
    """
    if organic is not None:
        organic = re.sub(r',', r'.', organic)
        organic = float(re.search(r'\d+[.]?\d*', organic)[0])

    return organic


def get_calories(calories):
    """
    Метод обработки значений калорий из данных "EcoMarket" по каждому продукту
    """
    if calories is not None:
        calories = float(re.search(r'\d+', calories)[0])

    return calories


def get_products():
    """
    Сохранение в БД данные по продуктам и их категориям от "EcoMarket"
    """
    r = requests.get("https://ecomarket.ru/public/goods_202110281305.xml")
    if r.status_code == 200:
        data = xmltodict.parse(r.content)                       # парсинг xml-данных в dict формат
        json_data = json.dumps(data, ensure_ascii=False)
        work_data = json.loads(json_data)                       # перевод данных в формат JSON
        # проходим циклом по всем категориям товаров
        for category in work_data['goods_data']['categories']['category']:                 # проходим по всем категориям
            if not CategoryProduct.objects.filter(shop_id=int(category['id'])).exists():   # если категории еще нет в БД
                category = CategoryProduct(shop_id=int(category['id']),                    # создаем категорию для БД
                                           name=category['name'],
                                           shop='EcoMarket')
                category.save()                                                            # сохраняем категорию в БД

        for product in work_data['goods_data']['offers']['offer']:      # проходим по всем продуктам
            if get_measure(product['name']) is not None:                # если мера веса/объема не равна None
                # print(product['name'])
                # print(product['weight_netto'], get_measure(product['name']))
                # print(product['category_id'], CategoryProduct.objects.get(shop_id=int(product['category_id'])))
                # print('--------------------------------------------------------------')
                product_db = Product(
                    shop='EcoMarket',
                    category=CategoryProduct.objects.get(shop_id=int(product['category_id'])),
                    shop_id=int(product['id']),
                    name=product['name'],
                    picture=product['images']['image']['image_url'],
                    proteins=get_organic(product['product_info']['proteins']),
                    fats=get_organic(product['product_info']['fats']),
                    carbohydrates=get_organic(product['product_info']['carbohydrates']),
                    calories=get_calories(product['product_info']['calories']),
                    qty_per_item=float(product['weight_netto']),
                    unit=get_measure(product['name']),
                    price=15.00              # цен на продукты нет в фидах ЭкоМаркета, для расчетов цена = 15
                )
                product_db.save()


def clear_data():
    """
    Очистить все записи в таблице Product
    """
    Product.objects.all().delete()


class Command(BaseCommand):
    def handle(self, *args, **options):
        clear_data()
        get_products()
        print("---------------------------------------PRODUCTS WAS ADDED----------------------------------------------")