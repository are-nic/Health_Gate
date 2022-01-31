from django.urls import path
from rest_framework.routers import SimpleRouter
from rest_framework_nested import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from food.views import (RecommendRecipesListView,
                        IngredientRecipeView,
                        IngredientListView,
                        CategoryAndKitchenView,
                        CommentView,
                        ProductView,
                        CookStepView,
                        RecipeViewSet,
                        TagViewSet,
                        FilterView)

from order.views import (OrderViewSet,
                         OrderRecipeViewSet,
                         OrderRecipeView,
                         # OrderProductView,
                         MealPlanRecipeView)

from user.views import UserView, CurrentUserView

router = SimpleRouter(trailing_slash=False)

# вложенные маршруты к заказам и рецептам заказа
# /order - все заказы тукущего пользователя
# /orders/{pk} - детали заказа по id
router.register('orders', OrderViewSet, basename='orders')
# /orders/{orders_pk}/recipe - все рецепты заказа
orders_router = routers.NestedSimpleRouter(router, 'orders', lookup='orders')
# /order/{order_pk}/recipe/{recipe_pk} - детали рецепта по id рецепта
orders_router.register('recipe', OrderRecipeViewSet, basename='recipe')

# вложенные маршруты к заказам через пользователя
# /users - все аккаунты доступные для Superuser или аккаунт текущего Юзера
# /users/{pk} - детали аккаунта
router.register('users', UserView, basename='users')
# /users/{users_pk}/user-orders - все заказы пользователя
users_router = routers.NestedSimpleRouter(router, 'users', lookup='users')
# /users/{users_pk}/user-orders/{order_pk} - детали заказа по id заказа
users_router.register('user-orders', OrderViewSet, basename='user-orders')

router.register('order-recipes', OrderRecipeView)
# router.register('order-products', OrderProductView)

router.register('products', ProductView)
router.register('recipes', RecipeViewSet)
router.register('steps', CookStepView)
router.register('ingredients', IngredientRecipeView, basename='ingredients')    # ингредиенты рецепта
router.register('comments', CommentView)

router.register('meal-plan', MealPlanRecipeView)

router.register('tags', TagViewSet)

router.register('current-user', CurrentUserView)

urlpatterns = [
    path('recipes-recommend', RecommendRecipesListView.as_view()),
    path('ingredients-list', IngredientListView.as_view()),     # список всех ингредиентов
    path('filters', FilterView.as_view()),
    path('extra-data', CategoryAndKitchenView.as_view()),
    path('token', TokenObtainPairView.as_view()),
    path('token/refresh', TokenRefreshView.as_view()),
    path('token/verify', TokenVerifyView.as_view()),
]
urlpatterns += router.urls
urlpatterns += orders_router.urls
urlpatterns += users_router.urls
