from django.urls import path, include
from rest_framework.routers import SimpleRouter

from .views import RecipeListView, RecipeDetailView, IngredientCreateView, UserView

router = SimpleRouter()
router.register('users', UserView)

urlpatterns = [
    path('recipes', RecipeListView.as_view()),
    path('recipes/<int:pk>/', RecipeDetailView.as_view()),
    path('ingredient/', IngredientCreateView.as_view()),
    # path('auth/', include('rest_framework.urls')),
    # path('auth/', include('djoser.urls')),
    # path('auth/', include('djoser.urls.authtoken')),
    # path('auth/', include('djoser.urls.jwt')),
]
urlpatterns += router.urls