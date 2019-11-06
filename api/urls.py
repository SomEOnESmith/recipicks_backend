from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView
from .views import (
	UserCreateAPIView, ProfileView, RecipeListView,
 	RecipeDetailView, IngredientListView,, CuisineListView
 )

urlpatterns = [
    path('login/', TokenObtainPairView.as_view() , name='login'),
    path('register/', UserCreateAPIView.as_view(), name='register'),
    path("profile/", ProfileView.as_view(), name="profile"),
    path('recipes/', RecipeListView.as_view(), name='recipes-list'),
    path('recipes/<int:recipe_id>/', RecipeDetailView.as_view(), name='recipe-detail'),
    path('ingredients/', IngredientListView.as_view(), name='ingredients-list'),
    path('recipes/ingredients/', RecipeListView.as_view(), name='recipes-ingredients'),
    path('cuisines/', CuisineListView.as_view(), name='cuisine-list')
]