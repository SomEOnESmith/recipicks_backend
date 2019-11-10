from rest_framework.generics import (
	CreateAPIView, ListAPIView, RetrieveAPIView, RetrieveUpdateAPIView,
)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter
from rest_framework.status import HTTP_200_OK
from json import loads
# Optimizing Search imports
from django.core import serializers
# import json
import numpy as np
import pandas as pd
from numba import njit

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


@njit
def divide(a, b):
    res = np.empty(a.shape)
    for i in range(len(a)):
        if b[i] != 0:
            res[i] = a[i] / b[i]
        else:
            res[i] = 0
    return res


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
		if cuisine:
			recipes = recipes.filter(cuisine=cuisine)
		if meals:
			recipes = recipes.filter(meal__in=meals)
		if courses:
			recipes = recipes.filter(course__in=courses)
		context = {'request': request}
		if not ingredients:
			return Response(self.serializer_class(recipes, context=context, many=True).data)
		recipes = recipes.filter(ingredients__in=ingredients).distinct()

		print(np.array(self.serializer_class(recipes, context=context, many=True).data))

		# print(list(recipes.values()))
		# df = pd.DataFrame(list(recipes.values()))

		# json_data = loads(serializers.serialize("json", recipes))
		# print(json_data)

		# recipes_array = np.array(json_data)

		# print(recipes_array)

		# print(recipes_array[0])
		# print(recipes_array[0]['fields']['ingredients'])
		# print(recipes_array[recipes_array['fields']['ingredients'].length > 1])

		# df2 = pd.DataFrame(json_data)
		# df3 = pd.DataFrame(df2.fields)

		# print(df2.fields[0]['ingredients'])
		# print(df2.fields)
		# print([data['fields'] for data in json_data])

		# print(list(map(json_data['fields'], json_data)))

		# print(df2)

		results = self.filter_by_ingredients(recipes=recipes, user_ingredients=set(ingredients))
		recipes = np.array(list(recipes.values()))
		
		# print(recipes)
		# print(df)
		# print(df[df['id']==1])

		# print(df2[set(df2.fields.ingredients.values_list('id', flat=True)) == set(ingredients)])
		# print(recipes[recipes.id == 1])
		# print(recipes[ set(recipes.ingredients.values_list('id', flat=True)) == set(ingredients) ] )

		data = {
			'perfect_match': self.serializer_class(results['perfect'], context=context, many=True).data,
			'user_excess_ingrs': self.serializer_class(results['excess'], context=context, many=True).data,
			'user_missing_ingrs': self.serializer_class(results['missing'], context=context, many=True).data
		}
		return Response(data, status=HTTP_200_OK)


class RecipeCreateAPIView(CreateAPIView):
	serializer_class = RecipeSerializer
	permission_classes = [IsAuthenticated]
