"""
Для запуска скрипта - python manage.py products
"""

from ...models import CategoryProduct, Product
from django.core.management.base import BaseCommand
import xmltodict
import json
import requests
import re


def get_qty_and_measure(name):
    """
    Метод нахождения меры веса или объема товара и его кол-во в имени товара с помощью регулярных выражений
    """
    qty_for_db = {'qty': 1.0, 'measure': 'кг.'} # передаваемый словарь с данными по кол-ву товара и его мере веса/объема
    pattern = r"[0-9]*[.,]?[0-9]{1,3}[ ]?(?:кг|гр|г|ГР|л|мл|шт|штук)\b"
    if len(re.findall(pattern, name)) == 1:      # если кол-во найденых мер веса и объема в имени одного товара равно 1
        qty_product = re.search(pattern, name)   # находим кол-во товара и его меру веса/объема

        qty_pattern = r"[0-9]*[.,]?[0-9]{1,3}"                  # паттерн для поиска количества товара
        qty = re.search(qty_pattern, qty_product[0])            # объект match найденого кол-ва продукта

        measure_pattern = r"(?:кг|гр|г|ГР|л|мл|шт|штук)\b"      # паттерн для поиска меры веса/объема
        measure = re.search(measure_pattern, qty_product[0])    # объект match найденой меры веса/объема

        if qty[0][0] == '.':        # если в начале найденого кол-ва товара точка, убираем её
            qty = qty[0][1:]        # кол-во товара равно найденому значению без точки в начале строки
        else:
            qty = qty[0]
        if ',' in qty:
            qty = float(re.sub(r',', r'.', qty))
        elif '.' in qty:
            qty = float(qty)
        qty_for_db['qty'] = float(qty)
        qty_for_db['measure'] = measure[0]
        return qty_for_db
    elif "1 десяток" in name:
        qty_for_db['qty'] = 10.0
        qty_for_db['measure'] = 'шт'
        return qty_for_db
    elif "вес" in name:
        return qty_for_db


def get_products():
    """
    Получение категорий продуктов и продуктов "Bringstone"
    Заносит в БД данные по магазинам и продуктам
    """
    r = requests.get("https://bringston.ru/include/KitchenFid.xml")
    if r.status_code == 200:
        data = xmltodict.parse(r.content)                   # парсинг xml-данных в dict формат
        json_data = json.dumps(data, ensure_ascii=False)
        work_data = json.loads(json_data)
        # проходим циклом по всем категориям товаров
        for category in work_data['yml_catalog']['shop']['categories']['category']:
            if not CategoryProduct.objects.filter(id=int(category['@id'])).exists():      # если категории еще нет в БД
                category = CategoryProduct(id=int(category['@id']), name=category['#text'])  # создаем категорию в БД
                category.save()                                                              # сохраняем категорию в БД

        for product in work_data['yml_catalog']['shop']['offers']['offer']:
            print(product['name'])
            print(get_qty_and_measure(product['name']))
            '''product_db = Product(
                category=CategoryProduct.objects.get(id=product['categoryId']),
                name=product['name'],
                picture=product['picture'],
                protein=product['param'][2]['#text'],
                fat=product['param'][1]['#text'],
                carbohydrates=product['param'][3]['#text'],
                calories=product['param'][0]['#text'],
                qty_per_item=product['valuecount'],
                price=product['price'],
                unit=product['value']['name']
            )
            product_db.save()'''


def clear_data():
    """
    Очистить все записи в таблице Product
    """
    Product.objects.all().delete()


class Command(BaseCommand):
    def handle(self, *args, **options):
        clear_data()
        get_products()
        print("Продукты занесены в БД")

"""
{
    "yml_catalog": {
        "@date": "2021-11-02 13:02", 
        "shop": {
            "name": "Bringston", 
            "company": "ООО «АЛИМОНИА»", 
            "url": "https://bringston.ru", 
            "platform": "1C-Bitrix", 
            "currencies": {
                "currency": {
                    "@id": "RUB", 
                    "@rate": "1"
                }
            }, 
            "categories": {
                "category": [
                    {
                        "@id": "16", 
                        "@parentId": "", 
                        "#text": "Азиатская кухня"
                    }, 
                    {
                        "@id": "17", 
                        "@parentId": "", 
                        "#text": "Бакалея"
                    }, 
                    {
                        "@id": "19", 
                        "@parentId": "17", 
                        "#text": "Крупы"
                    }, 
                    {
                        "@id": "20", 
                        "@parentId": "17", 
                        "#text": "Макароны"
                    }
                ]
            },
"""