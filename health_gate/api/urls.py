from django.urls import path
from rest_framework.routers import SimpleRouter
from rest_framework_nested import routers

from food.views import (RecommendRecipesListView,
                        IngredientView,
                        CommentView,
                        ProductView,
                        CookStepView,
                        RecipeViewSet)

from order.views import (OrderViewSet,
                         OrderRecipeViewSet,
                         OrderListView,
                         OrderDetailView,
                         OrderRecipeView,
                         OrderProductView,
                         MealPlanRecipeView)

from user.views import UserView

router = SimpleRouter(trailing_slash=False)

# альтернативные маршруты к заказам и рецептам заказа
# /order - все заказы тукущего пользователя
# /order/{pk} - детали заказа по id
router.register('order', OrderViewSet, basename='order')
# /order/{order_pk}/recipe - все рецепты заказа
order_router = routers.NestedSimpleRouter(router, 'order', lookup='order')
# /order/{order_pk}/recipe/{recipe_pk} - детали рецепта по id рецепта
order_router.register('recipe', OrderRecipeViewSet, basename='recipe')

# вложенные маршруты к заказам через пользователя
# /users - все аккаунты доступные для Superuser или аккаунт текущего Юзера
# /users/{pk} - детали аккаунта
router.register('users', UserView, basename='users')
# /users/{users_pk}/user-orders - все заказы пользователя
users_router = routers.NestedSimpleRouter(router, 'users', lookup='users')
# /users/{users_pk}/user-orders/{order_pk} - детали заказа по id заказа
users_router.register('user-orders', OrderViewSet, basename='user-orders')

router.register('order-recipes', OrderRecipeView)
router.register('order-products', OrderProductView)

router.register('products', ProductView)
router.register('recipes', RecipeViewSet)
router.register('steps', CookStepView)
router.register('ingredients', IngredientView, basename='ingredients')
router.register('comments', CommentView)

router.register('meal-plan', MealPlanRecipeView)

urlpatterns = [
    path('recipes-recommend', RecommendRecipesListView.as_view()),
    path('orders', OrderListView.as_view()),
    path('orders/<int:pk>', OrderDetailView.as_view())
]
urlpatterns += router.urls
urlpatterns += order_router.urls
urlpatterns += users_router.urls
