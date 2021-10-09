from django.urls import path
from rest_framework.routers import SimpleRouter

from .views import (RecipeListView,
                    RecipeDetailView,
                    RecommendRecipesListView,
                    IngredientView,
                    CommentView,
                    UserView,
                    OrderListView,
                    OrderDetailView,
                    OrderRecipeView,
                    OrderProductView,
                    ProductView)

router = SimpleRouter(trailing_slash=False)
router.register('users', UserView)
router.register('comments', CommentView)
router.register('ingredients', IngredientView)
router.register('order-recipes', OrderRecipeView)
router.register('order-product', OrderProductView)
router.register('products', ProductView)

urlpatterns = [
    path('recipes', RecipeListView.as_view()),
    path('recipes/<int:pk>', RecipeDetailView.as_view()),
    path('recipes-recommend', RecommendRecipesListView.as_view()),
    path('orders', OrderListView.as_view()),
    path('orders/<int:pk>', OrderDetailView.as_view())
]
urlpatterns += router.urls
