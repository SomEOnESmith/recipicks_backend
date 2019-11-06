from rest_framework.generics import (
	CreateAPIView, ListAPIView, RetrieveAPIView, RetrieveUpdateAPIView,
)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter

from .serializers import (
	UserCreateSerializer, CreateUpdateProfileSerializer, RecipeDetailsSerializer,
	RecipesListSerializer, IngredientSerializer, CuisineSerializer
)
from .models import Recipe, Profile, Ingredient, Cuisine 


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
		exact_match = [recipe for recipe in recipes if set(recipe.ingredients.values_list('id',flat=True))==set(request.data)]
		user_has_excess = [recipe for recipe in recipes if set(recipe.ingredients.values_list('id',flat=True)).issubset(request.data) and recipe not in exact_match]
		user_has_missing = list(set(recipes).difference(exact_match, user_has_excess))
		data = {
			'exact_match': RecipesListSerializer(exact_match, context={'request': request}, many=True).data,
			'user_has_excess_ingredients': RecipesListSerializer(user_has_excess, context={'request': request}, many=True).data,
			'user_has_missing_ingredients': RecipesListSerializer(user_has_missing, context={'request': request}, many=True).data
		}
		return Response(data, status=200)


class CuisineListView(ListAPIView):
	queryset = Cuisine.objects.all()
	serializer_class = CuisineSerializer


