from rest_framework.generics import (
	CreateAPIView, ListAPIView, RetrieveAPIView, RetrieveUpdateAPIView,
)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter
from rest_framework.status import HTTP_200_OK

from .serializers import (
	UserCreateSerializer, CreateUpdateProfileSerializer, RecipeDetailSerializer,
	RecipeListSerializer, IngredientSerializer
)
from .models import Recipe, Profile, Ingredient


class UserCreateAPIView(CreateAPIView):
	serializer_class = UserCreateSerializer


class ProfileView(RetrieveUpdateAPIView):
	serializer_class = CreateUpdateProfileSerializer
	permission_classes = [IsAuthenticated]

	def get_object(self):
		return self.request.user.profile


class RecipeDetailView(RetrieveAPIView):
	queryset = Recipe.objects.all()
	serializer_class = RecipeDetailSerializer
	lookup_field = 'id'
	lookup_url_kwarg = 'recipe_id'


class IngredientListView(ListAPIView):
	queryset = Ingredient.objects.all()
	serializer_class = IngredientSerializer


class RecipeListView(APIView):
	serializer_class = RecipeListSerializer
	filter_backends = [SearchFilter,]
	search_fields = ['title','meal__name', 'cuisine__name', 'course__name']

	def search(self, recipes, ingredients):
		results = {'exact': [], 'excess': [], 'missing': []}
		for recipe in recipes:
			ingredients = recipe.ingredients.values_list('id', flat=True)
			if ingredients ==ingredients:
				results['exact'].append(recipe)
			elif set(ingredients).issubset(ingredients):
				results['excess'].append(recipe)
			else:
				results['missing'].append(recipe)
		return results

	def get(self,request):
		meal = request.GET.get("meal")
		cuisine = request.GET.get("cuisine")
		course = request.GET.get("course")
		ingredients = request.GET.getlist("ingredients[]")
		context = {'request': request}
		if not ingredients:
			return Response(self.serializer_class(Recipe.objects.all(), context=context, many=True).data)
		recipes = Recipe.objects.filter(ingredients__id__in=ingredients).distinct()
		results = self.search(recipes=recipes, ingredients=ingredients)
		data = {
			'perfect_match': self.serializer_class(results['exact'], context=context, many=True).data,
			'user_excess_ings': self.serializer_class(results['excess'], context=context, many=True).data,
			'user_missing_ings': self.serializer_class(results['missing'], context=context, many=True).data
		}
		return Response(data, status=HTTP_200_OK)
