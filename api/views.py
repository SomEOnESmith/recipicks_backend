from rest_framework.generics import (
	CreateAPIView, ListAPIView, RetrieveAPIView, RetrieveUpdateAPIView,
)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter
from rest_framework.status import HTTP_200_OK
from json import loads

from .serializers import (
	UserCreateSerializer, CreateUpdateProfileSerializer, RecipeDetailSerializer,
	RecipeListSerializer, IngredientSerializer, CuisineSerializer, CourseSerializer,
	MealSerializer, RecipeSerializer
)
from .models import Recipe, Profile, Ingredient, Cuisine, Course, Meal


class UserCreateAPIView(CreateAPIView):
	serializer_class = UserCreateSerializer


class ProfileView(RetrieveUpdateAPIView):
	serializer_class = CreateUpdateProfileSerializer
	permission_classes = [IsAuthenticated]

	def get_object(self):
		return self.request.user.profile


class FilterView(APIView):
	def get(self, request):
		data = {
			'ingredients': IngredientSerializer(Ingredient.objects.all(), many=True).data,
			'cuisines': CuisineSerializer(Cuisine.objects.all(), many=True).data,
			'courses': CourseSerializer(Course.objects.all(), many=True).data,
			'meals': MealSerializer(Meal.objects.all(), many=True).data
		}
		return Response(data, status=HTTP_200_OK)


class RecipeDetailView(RetrieveAPIView):
	queryset = Recipe.objects.all()
	serializer_class = RecipeDetailSerializer
	lookup_field = 'id'
	lookup_url_kwarg = 'recipe_id'


class RecipeListView(APIView):
	serializer_class = RecipeListSerializer

	def filter_by_ingredients(self, recipes, user_ingredients):
		results = {'perfect': [], 'excess': [], 'missing': []}
		for recipe in recipes:
			recipe_ingredients = set(recipe.ingredients.values_list('id', flat=True))
			if recipe_ingredients == user_ingredients:
				results['perfect'].append(recipe)
			elif recipe_ingredients.issubset(user_ingredients):
				results['excess'].append(recipe)
			else:
				results['missing'].append(recipe)
		return results

	def get(self,request):
		recipes = Recipe.objects.all()
		cuisine = request.GET.get("cuisine")
		meals = loads(request.GET.get("meals"))
		courses = loads(request.GET.get("courses"))
		ingredients = loads(request.GET.get("ingredients"))
		print(meals,courses,cuisine)
		if cuisine:
			recipes = recipes.filter(cuisine=cuisine)
		if meals:
			recipes = recipes.filter(meal__in=meals)
		if courses:
			recipes = recipes.filter(course__in=courses)
		context = {'request': request}
		if not ingredients:
			return Response(self.serializer_class(recipes, context=context, many=True).data)
		recipes = recipes.filter(ingredients__id__in=ingredients).distinct()
		results = self.filter_by_ingredients(recipes=recipes, user_ingredients=set(ingredients))
		data = {
			'perfect_match': self.serializer_class(results['perfect'], context=context, many=True).data,
			'user_excess_ingrs': self.serializer_class(results['excess'], context=context, many=True).data,
			'user_missing_ingrs': self.serializer_class(results['missing'], context=context, many=True).data
		}
		return Response(data, status=HTTP_200_OK)


class RecipeCreateAPIView(CreateAPIView):
	serializer_class = RecipeSerializer
	permission_classes = [IsAuthenticated]