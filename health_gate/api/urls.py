from django.urls import path, include
from rest_framework.routers import SimpleRouter
from rest_framework_nested import routers

from food.views import (RecommendRecipesListView,
                        IngredientView,
                        CommentView,
                        ProductView,
                        CookStepsByRecipeView,
                        CookStepDetailView,
                        RecipeListView,
                        RecipeDetailView)

from order.views import (OrderViewSet,
                         OrderRecipeViewSet,
                         OrderListView,
                         OrderDetailView,
                         OrderRecipeView,
                         OrderProductView)

from user.views import UserView

router = SimpleRouter(trailing_slash=False)

# альтернативный доступ к заказам и рецептам заказа
# /order - все заказы тукущего пользователя
# /order/1 - детали заказа по id = 1
# /order/1/recipe - все рецепты заказа по id = 1
# /order/1/recipe/2 - детали рецепта по id = 2 заказа по id = 1
router.register('order', OrderViewSet, basename='order')
order_router = routers.NestedSimpleRouter(router, 'order', lookup='order')
order_router.register('recipe', OrderRecipeViewSet, basename='recipe')

router.register('users', UserView)
router.register('comments', CommentView)
router.register('ingredients', IngredientView, basename='ingredients')
router.register('order-recipes', OrderRecipeView)
router.register('order-product', OrderProductView)
router.register('products', ProductView)


urlpatterns = [
    path('recipes', RecipeListView.as_view()),
    path('recipes/<int:pk>', RecipeDetailView.as_view()),
    path('recipes-recommend', RecommendRecipesListView.as_view()),
    path('steps', CookStepsByRecipeView.as_view()),
    path('steps/<int:pk>', CookStepDetailView.as_view()),
    path('orders', OrderListView.as_view()),
    path('orders/<int:pk>', OrderDetailView.as_view())
]
urlpatterns += router.urls
urlpatterns += order_router.urls