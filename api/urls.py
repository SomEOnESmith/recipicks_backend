from django.urls import path
from .views import (RecipeListView, RecipeDetailsView)


urlpatterns = [
    path('recipes/', RecipeListView.as_view(), name='recipes-list'),
    path('recipes/<int:recipe_id>/', RecipeDetailsView.as_view(), name='recipe-detail'),

]