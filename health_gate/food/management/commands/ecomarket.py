"""
Парсер данных по продуктам из Экомаркета. В БД попадают продукты, относящиеся к категориям, не входящим в список
непродуктовых категорий.
Для запуска обновления продуктов в БД из "EcoMarket" - python manage.py ecomarket
Для автообноления БД на сервере используется Corn, который через заданные промежутки времени запускает скрипт
"""

from ...models import CategoryProduct, Product, Ingredient
from django.core.management.base import BaseCommand
import csv
import re
import requests
import difflib as dl
from .products_lists import *


def get_qty_and_measure(name):
    """
    Метод нахождения меры веса или объема товара и его кол-во в имени товара.
    :return словарь с ключами 'qty' - кол-во и 'measure' - мера
    """
    qty_for_db = {'qty': 1.0, 'measure': 'кг.'}     # словарь с данными по кол-ву товара и его мере веса/объема

    pattern = r"[0-9]*[.,]?[0-9]{1,3}[ ]?(?:кг|гр|г|ГР|л|мл|шт|штук)\b"

    if len(re.findall(pattern, name)) == 1:      # если кол-во найденных мер веса и объема в имени одного товара равно 1
        qty_product = re.search(pattern, name)   # находим кол-во товара и его меру веса/объема

        qty_pattern = r"[0-9]*[.,]?[0-9]{1,3}"                  # паттерн для поиска количества товара
        qty = re.search(qty_pattern, qty_product[0])            # объект match найденного кол-ва продукта

        measure_pattern = r"(?:кг|гр|г|ГР|л|мл|шт|штук)\b"      # паттерн для поиска меры веса/объема
        measure = re.search(measure_pattern, qty_product[0])    # объект match найденной меры веса/объема

        if qty[0][0] == '.':        # если в начале найденного кол-ва товара точка, убираем её
            qty = qty[0][1:]        # кол-во товара равно найденному значению без точки в начале строки
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


def get_organic(organic):
    """
    Метод обработки значений белков, жиров, углеводов из данных "EcoMarket" по каждому продукту
    Если в данных нет информации о БЖУ, сохраняет Ноль
    """
    if organic != '' and organic is not None:
        organic = re.sub(r',', r'.', organic)
        organic = float(re.search(r'\d+[.]?\d*', organic)[0])

        return organic
    return 0


def get_calories(calories):
    """
    Метод обработки значений калорий из данных "EcoMarket" по каждому продукту
    Если в данных нет информации о калориях, сохраняет Ноль
    """
    if calories != '' and calories is not None:
        calories = float(re.search(r'\d+', calories)[0])

        return calories
    return 0


def get_clear_product(product):
    pattern = r'\b[а-яА-ЯёЁ ]+'
    product = re.search(pattern, product)[0].split(' ')[:2]
    product = ' '.join(product)
    return product


def create_product(product, match):
    """
    Создаем и сохраняем продукт.
    :param product: продукт, который нужно создать.
    :param match: первый ингредиент из списка совпадений.
    """
    product_db = Product(
        ingredient=Ingredient.objects.get(name=match),
        shop=product['shop'],
        category=CategoryProduct.objects.get(name=product['category']),
        shop_id=int(product['id']),
        name=product['name'],
        picture=product['picture'],
        proteins=get_organic(product['proteins']),
        fats=get_organic(product['fats']),
        carbohydrates=get_organic(product['carbohydrates']),
        calories=get_calories(product['calories']),
        qty_per_item=float(get_qty_and_measure(product['name'])['qty']),
        unit=get_qty_and_measure(product['name'])['measure'],
        price=float(product['price'])
    )
    product_db.save()


def get_products():
    """
    Сохранение в БД данные по продуктам и их категориям от "EcoMarket"
    """
    """
        ;                                                                                           -1
        ;                                                                                           -2
        ;                                                                                           -3
        ;                                                                                           -4
        7722;                                                                                       - id
        "Фрикадельки фалафель Ecomarket.ru - 200 г";                                                - name
        ;                                                                                           -7
        Ecomarket;                                                                                  - shop
        шт;                                                                                         - min_unit
        1;                                                                                          - min_gty
        ;                                                                                           -11
        4;                                                                                          - available_qty
        195.8;                                                                                      - price
        ;                                                                                           -14
        https://ecomarket.ru/imgs/products_w/7722/thumb/frikadelki-falafel---200-g-1.1611871.jpg;   - picture
        ;                                                                                           -16
        "8,3 г.";                                                                                   - proteins
        "1,9 г.";                                                                                   - fats
        "19,3 г.";                                                                                  - carbohydrates
        "127 кКал.";                                                                                - calories
        "Полуфабрикаты ";                                                                           - category
        0.2                                                                                         - qty_per_item (кг)
    """
    res = requests.get("https://ecomarket.ru/public/kitchen_full_78.csv")
    if res.status_code == 200:
        fieldnames = [
            1,
            2,
            3,
            4,
            'id',
            'name',
            7,
            'shop',
            'min_unit',
            'min_qty',
            11,
            'available_qty',
            'price',
            14,
            'picture',
            16,
            'proteins',
            'fats',
            'carbohydrates',
            'calories',
            'category',
            'qty'
        ]

        i = 0       # счетчик ингредиентов
        j = 0       # счетчик продуктов
        ingredients = [str(ingredient) for ingredient in Ingredient.objects.all()]

        products = res.content.decode('utf-8').split('\n')
        reader = csv.DictReader(products, delimiter=';', fieldnames=fieldnames)
        for product in reader:
            j += 1      # увеличиваем счетчик продуктов
            # если категория не в списке недопустимых категорий товаров и ее еще нет в БД
            if product['category'] not in invalid_category and \
                    not CategoryProduct.objects.filter(name=product['category']).exists():
                category = CategoryProduct(name=product['category'], shop=product['shop'])  # создаем категорию
                category.save()                                                             # сохраняем категорию в БД

            # если категория не в списке недопустимых категорий товаров
            # и в имени продукта есть пограммовка, создаем и сохраняем продукт
            if product['category'] not in invalid_category and get_qty_and_measure(product['name']) is not None:
                # убираем из имени продукта лишнее
                clear_product = get_clear_product(product['name'])
                # проверка сходства между продуктом и ингредиентами
                match = dl.get_close_matches(clear_product, ingredients, cutoff=0.8)
                if len(match) > 0:  # если найдены сходства ингредиента с названием продукта
                    print(match[0], '--ингредиент--')
                    print(product['name'])
                    print('-------------------------------------------------')
                    i += 1  # увеличиваем счетчик ингредиентов
                    # создаем и сохраняем продукт
                    create_product(product, match[0])
                elif clear_product != ' ':  # если имя продукта непустое
                    match = dl.get_close_matches(clear_product.split()[0], ingredients, cutoff=0.8)
                    if len(match) > 0:
                        print(match[0], '--ингредиент--')
                        print(product['name'])
                        print('-------------------------------------------------')
                        i += 1
                        # создаем и сохраняем продукт
                        create_product(product, match[0])

        print(i, 'ingredients')
        print(j, 'products')


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