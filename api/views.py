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
from rest_framework.filters import SearchFilter


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
	filter_backends = [SearchFilter,]
	search_fields = ['title','meal__name', 'cuisine__name', 'course__name']


class RecipeDetailsView(RetrieveAPIView):
	queryset = Recipe.objects.all()
	serializer_class = RecipeDetailsSerializer
	lookup_field = 'id'
	lookup_url_kwarg = 'recipe_id'


class IngredientsListView(ListAPIView):
	queryset = Ingredient.objects.all()
	serializer_class = IngredientSerializer


class RecipesByIngredientListView(APIView):
	def post(self,request):
		recipes = Recipe.objects.filter(ingredients__id__in=request.data).distinct()
		filtered_recipes = [recipe for recipe in recipes if set(recipe.ingredients.values_list('id',flat=True)).issubset(request.data)]
		return Response(RecipesListSerializer(filtered_recipes, many=True).data)



