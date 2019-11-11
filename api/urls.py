from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView
from .views import (
	FilterView, ProfileView, RecipeCreateAPIView,
	RecipeDetailView, RecipeListView, UserCreateAPIView 
)

urlpatterns = [
	path('login/', TokenObtainPairView.as_view() , name='login'),
	path('register/', UserCreateAPIView.as_view(), name='register'),
	path("profile/", ProfileView.as_view(), name="profile"),
	path('filters/', FilterView.as_view(), name='filters'),
	path('recipes/', RecipeListView.as_view(), name='recipes-list'),
	path('recipes/<int:recipe_id>/', RecipeDetailView.as_view(), name='recipe-detail'),
	path('recipe/create/', RecipeCreateAPIView.as_view(), name='recipe-create')
]