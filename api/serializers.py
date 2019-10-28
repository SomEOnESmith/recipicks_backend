from rest_framework import serializers
from .models import (Recipe, Cuisine, Ingredient, Course, Meal, Step)


class CuisineSerializer(serializers.ModelSerializer):
	class Meta:
		model = Cuisine
		fields = '__all__'

class IngredientSerializer(serializers.ModelSerializer):
	class Meta:
		model = Ingredient
		fields = '__all__'

class CourseSerializer(serializers.ModelSerializer):
	class Meta:
		model = Course
		fields = '__all__'

class MealSerializer(serializers.ModelSerializer):
	class Meta:
		model = Meal
		fields = '__all__'

class StepsSerializer(serializers.ModelSerializer):
	class Meta:
		model = Step
		fields = '__all__'

class RecipesListSerializer(serializers.ModelSerializer):
	class Meta:
		model = Recipe
		fields = ['id','title','image']

class RecipeDetailsSerializer(serializers.ModelSerializer):
	cuisine = CuisineSerializer()
	course = CourseSerializer(many=True)
	meal = MealSerializer(many=True)
	ingredients = IngredientSerializer(many=True)
	steps = StepsSerializer(many=True) 
	class Meta:
		model = Recipe
		fields =  ['id','title','description','image','cuisine','course','meal','ingredients', 'steps']
		


