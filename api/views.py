from rest_framework.generics import (
	CreateAPIView, ListAPIView, RetrieveAPIView, RetrieveUpdateAPIView,
)
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Count

from .serializers import (
	UserCreateSerializer, CreateUpdateProfileSerializer, RecipeDetailsSerializer,
	RecipesListSerializer, IngredientSerializer
)
from .models import Recipe, Profile, Ingredient
from rest_framework.permissions import IsAuthenticated


class UserCreateAPIView(CreateAPIView):
	serializer_class = UserCreateSerializer


class ProfileView(RetrieveUpdateAPIView):
	serializer_class = CreateUpdateProfileSerializer
	permission_classes = [IsAuthenticated]

	def get_object(self):
		return self.request.user.profile


class RecipeListView(ListAPIView):
	queryset = Recipe.objects.all()
	serializer_class = RecipesListSerializer
 

class RecipeDetailsView(RetrieveAPIView):
	queryset = Recipe.objects.all()
	serializer_class = RecipeDetailsSerializer
	lookup_field = 'id'
	lookup_url_kwarg = 'recipe_id'


class IngredientsListView(ListAPIView):
	queryset = Ingredient.objects.all()
	serializer_class = IngredientSerializer


class RecipesByMealListView(ListAPIView):
	serializer_class = RecipesListSerializer

	def get_queryset(self):
		return Recipe.objects.filter(meal__name=self.kwargs['meal_type'])	


class RecipesByCuisineListView(ListAPIView):
	serializer_class = RecipesListSerializer

	def get_queryset(self):
		return Recipe.objects.filter(cuisine__name=self.kwargs['cuisine_name'])


class RecipesByIngredientListView(APIView):
	def post(self,request):
		recipes = Recipe.objects.filter(ingredients__id__in=request.data).distinct()
		filtered_recipes = [recipe if set(recipe.ingredients.values_list('id',flat=True)).issubset(request.data) else None for recipe in recipes]
		return Response(RecipesListSerializer(filtered_recipes, many=True).data)



