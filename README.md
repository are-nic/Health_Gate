# Health_Gate API doc

----------------------------------------- ПОЛЬЗОВАТЕЛЬ ----------------------------------------

http://api.healthgate.club/api/v1/users

POST запросом отправляются обязательные параметры:

{

    "phone_number": "+79999999999",
    
    "password": "records0",
    
    "groups": ["bloger"],
    
    "tags": ["Расстройство пищеварения"]
    
}

При заполнении параметра groups указываются значения, которые заранее занесены в группы проекта через админку Django. (“bloger”, “customer”) 

При заполнении tags указываются значения, которые внесены в БД заранее

Пользователь Активный сразу после регистрации.

После регистрации возможен доступ к API по токену


Вывод всех пользователей доступен суперпользователю. Остальные могут получить только свои аккаунты и производить над ними действия. 
Доступны все методы: GET, POST, PUT, PATCH, DELETE
http://api.healthgate.club/api/v1/users/{id}


----------------------------------------- Доступ к API по токену -----------------------------------------
Заходим на http://api.healthgate.club/api/token/
Создаем POST запрос c двумя полями в Body:
phone_number: +79997007766
password: records0
Получаем в ответе два токена. Используем токен «access». Время жизни токена – 1 сутки 
(можно менять в settings.py - SIMPLE_JWT = {'ACCESS_TOKEN_LIFETIME': timedelta(days=1),...}).
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYzMzQyNDc2MywianRpIjoiY2RkMjRiOTNlNThhNGNmZGJiYTUyMWIwZjY4ZGJmYjkiLCJ1c2VyX2lkIjo3fQ.Cw6vITWBMr6V8FSzq6472FTDPU_FwshPPMKp9k-RnbM",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjMzMzM4NjYzLCJqdGkiOiI1NTI5ZjQzNzRlZDU0MmIxOTJmZGQ1MTZhYzIxMTA5YyIsInVzZXJfaWQiOjd9.83WoOKk0RXnEVZDOIWDmQB9uHhTpIw8342NazXMsjMs"
}

Переходим на вкладку запроса данных
В Headers добавляем поле Authorization
Значение поля: Bearer + access токен, который мы получили выше.
Например, так:
Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjMzMzM5NjAyLCJqdGkiOiJjODU0NzI0NDQzYjk0OTA5OTZjMWVlM2U1Zjk0YzgxZCIsInVzZXJfaWQiOjd9.fQmw_v9R6R794jYrMuDCCTlWX-7GX9BW8jB9eCHK5H0
Выполняем запрос:
http://api.healthgate.club/api/v1/recipes/
Получаем данные.

-----------------------------------------РЕЦЕПТЫ-----------------------------------------
Получение списка рецептов по рекомендациям (тегам)
Метод: GET
url: http://api.healthgate.club/api/v1/recipes-recommend

Получение списка всех рецептов, создание рецепта
Метод: GET, POST
url: http://api.healthgate.club/api/v1/recipes
Рецепты создаются при условии, что пользователь находится в группе «bloger», либо является суперпользователем
В JSON формате необходимые поля:
{
    "title": "Каша на топоре",
    "slug": "kasha-na-topore",
    "level": "HARD",
    "no_preservatives": true,
    "cooking_time": "60 минут",
    "protein": 34,
    "fat": 45,
    "carbohydrates": 12,
    "kkal": 400,
    "description": "Издревле национальная русская кухня. Каша на топоре",
    "image": null,
    "price": "770.00",
    "portions": 6,
    "category": "Десерты",
    "kitchen": "Континентальная",
    "tags": [
                "Здоровое старение"
            ]
}
Править или удалять рецепт может создатель рецепта либо суперпользователь 

Получение, обновление, частичное обновление или удаление одного рецепта по id
Метод: GET, PUT, PATCH, DELETE
url: http://api.healthgate.club/api/v1/recipes/{id}


-----------------------------------------ШАГИ ПРИГОТОВЛЕНИЯ РЕЦЕПТА-----------------------------------------
Список всех шагов всех рецептов может получить суперпользователь
Создатель рецепта получает доступ только к шагам приготовления своих рецептов

Получение списка всех шагов приготовления, создание шага
Метод: GET, POST
url: http://api.healthgate.club/api/v1/steps

Получение, обновление, частичное обновление или удаление шага приготовления по id
Метод: GET, PUT, PATCH, DELETE
url: http://api.healthgate.club/api/v1/steps/{id}


-----------------------------------------ИНГРЕДИЕНТЫ РЕЦЕПТА-----------------------------------------
Список всех ингредиентов всех рецептов может получить суперпользователь
Создатель рецепта получает доступ только к ингредиентам своих рецептов

Получение списка всех ингредиентов, добавление ингредиента
Метод: GET, POST
url: http://api.healthgate.club/api/v1/ingredients

Получение, обновление, частичное обновление или удаление шага ингредиента по id
Метод: GET, PUT, PATCH, DELETE
url: http://api.healthgate.club/api/v1/ingredients/{id}

-----------------------------------------КОММЕНТАРИИ К РЕЦЕПТАМ-----------------------------------------
Список всех комментариев всех рецептов может получить суперпользователь
Пользователи могут создавать, править, удалять комментарии к рецептам. 
Вывод комментариев для пользователей доступен в составе рецепта или по id для совершения действий над ними. Действия над комментарием могу производить только авторы коммента либо суперюзер.

Получение списка всех комментариев, добавление комментария
Метод: GET, POST
url: http://api.healthgate.club/api/v1/comments

Получение, обновление, частичное обновление или удаление комментария по id
Метод: GET, PUT, PATCH, DELETE
url: http://api.healthgate.club/api/v1/comments/{id}

-----------------------------------------ПРОДУКТ-----------------------------------------
Действия над продуктом доступны только суперпользователю

Получение списка всех продуктов, добавление продукта
Метод: GET, POST
url: http://api.healthgate.club/api/v1/products 

Получение, обновление, частичное обновление или удаление продукта по id
Метод: GET, PUT, PATCH, DELETE
url: http://api.healthgate.club/api/v1/products/{id}

-----------------------------------------ЗАКАЗ-----------------------------------------
Список всех заказов всех пользователей доступен суперюзеру
Пользователю доступны только его заказы и действия над ними

Получение списка всех заказов, добавление заказа
Метод: GET, POST
url: http://api.healthgate.club/api/v1/orders 

Получение, обновление, частичное обновление или удаление заказа по id
Метод: GET, PUT, PATCH, DELETE
url: http://api.healthgate.club/api/v1/orders/{id}

Вложенные маршруты к заказам через пользователя
{domain}/users/{users_pk}/user-orders - все заказы пользователя
{domain}/users/{users_pk}/user-orders/{order_pk} - детали заказа по id заказа

-----------------------------------------РЕЦЕПТ ЗАКАЗА-----------------------------------------
Список рецептов всех заказов всех пользователей доступен суперюзеру
Пользователю доступны только рецепты его заказов и действия над ними

Получение списка всех рецептов заказов, добавление рецепта заказа
Метод: GET, POST
url: http://api.healthgate.club/api/v1/order-recipes 

Получение, обновление, частичное обновление или удаление рецепта заказа по id
Метод: GET, PUT, PATCH, DELETE
url: http://api.healthgate.club/api/v1/order-recipes/{id}
Вложенные маршруты к рецептам заказа через заказ
{domain}/order/{order_pk}/recipe - все рецепты одного заказа
{domain}/ order/{order_pk}/recipe/{recipe_pk} - детали рецепта заказа

-----------------------------------------ПРОДУКТ ЗАКАЗА-----------------------------------------
Список продуктов всех заказов всех пользователей и действия над ними доступны суперюзеру.
Пользователю доступны только продукты его заказов и действия над ними.

Получение списка всех продуктов заказов, добавление продукта заказа
Метод: GET, POST
url: http://api.healthgate.club/api/v1/order-products

Получение, обновление, частичное обновление или удаление продукта заказа по id
Метод: GET, PUT, PATCH, DELETE
url: http://api.healthgate.club/api/v1/order-products/{id}


-----------------------------------------ПЛАН ПИТАНИЯ-----------------------------------------
Список планов всех пользователей и действия над ними доступны Суперюзеру.
Пользователю доступны только его планы и действия над ними.

Получение списка всех планов питания, добавление плана
Метод: GET, POST
url: http://api.healthgate.club/api/v1/meal-plan

Получение, обновление, частичное обновление или удаление продукта заказа по id
Метод: GET, PUT, PATCH, DELETE
url: http://api.healthgate.club/api/v1/meal-plan/{id}

