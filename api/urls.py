from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView
from .views import (UserCreateAPIView, RecipeListView, RecipeDetailsView)

urlpatterns = [
    path('login/', TokenObtainPairView.as_view() , name='login'),
    path('register/', UserCreateAPIView.as_view(), name='register'),
    path('recipes/', RecipeListView.as_view(), name='recipes-list'),
    path('recipes/<int:recipe_id>/', RecipeDetailsView.as_view(), name='recipe-detail'),
]