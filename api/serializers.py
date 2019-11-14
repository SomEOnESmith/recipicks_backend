from rest_framework import serializers
from django.contrib.auth.models import User
from drf_writable_nested import WritableNestedModelSerializer

from .models import Course, Cuisine, Image, Ingredient, Meal, Profile, Recipe, Step
from .base64 import decode_base64

class UserCreateSerializer(serializers.ModelSerializer):
	password = serializers.CharField(write_only=True)

	class Meta:
		model = User
		fields = ('username', 'password')

	def create(self, validated_data):
		new_user = User(**validated_data)
		new_user.set_password(validated_data['password'])
		new_user.save()
		return validated_data


class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'email')
		read_only_fields = ('username',)


class CreateUpdateProfileSerializer(serializers.ModelSerializer):
	user = UserSerializer()
	
	class Meta:
		model = Profile
		fields = '__all__'

	def update(self, instance, validated_data):
		user_field = validated_data.pop('user', None)
		temp_user_serializer = UserSerializer()
		super().update(instance, validated_data)
		super(UserSerializer, temp_user_serializer).update(instance.user, user_field)
		return instance


class CourseSerializer(serializers.ModelSerializer):
	class Meta:
		model = Course
		fields = '__all__'


class CuisineSerializer(serializers.ModelSerializer):
	class Meta:
		model = Cuisine
		fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):
	class Meta:
		model = Ingredient
		fields = '__all__'


class MealSerializer(serializers.ModelSerializer):
	class Meta:
		model = Meal
		fields = '__all__'


class StepSerializer(serializers.ModelSerializer):
	class Meta:
		model = Step
		fields = '__all__'


class RecipeDetailSerializer(serializers.ModelSerializer):
	cuisine = CuisineSerializer()
	courses = CourseSerializer(many=True)
	meals = MealSerializer(many=True)
	ingredients = IngredientSerializer(many=True)
	steps = StepSerializer(many=True)

	class Meta:
		model = Recipe
		fields =  '__all__'


class RecipeListSerializer(serializers.ModelSerializer):
	meals = MealSerializer(many=True)
	cuisine = CuisineSerializer()

	class Meta:
		model = Recipe
		exclude = ('description', 'courses')


class ImageSerializer(serializers.ModelSerializer):
	class Meta:
		model = Image
		fields = '__all__'


class StepCreateSerializer(serializers.ModelSerializer):
	class Meta:
		model = Step
		exclude = ('recipe', 'id')


class RecipeCreateSerializer(WritableNestedModelSerializer):
	steps = StepCreateSerializer(many=True)
	image = serializers.CharField()
	# images = ImageSerializer(many=True)

	class Meta:
		model = Recipe
		exclude = ('total_time',)

	def create(self, validated_data):
		title = validated_data['title']
		description = validated_data['description']
		courses = validated_data['courses']
		cuisine = validated_data['cuisine']
		ingredients = validated_data['ingredients']
		meals = validated_data['meals']
		steps = validated_data['steps']
		new_image = validated_data['image']
		data = decode_base64(new_image)
		new_recipe = Recipe.objects.create(
			title=title, description= description,
			cuisine=cuisine, image = data
		)
		new_recipe.courses.set(courses)
		new_recipe.meals.set(meals)
		new_recipe.ingredients.set(ingredients)
		new_recipe.save()
		recipe_object = Recipe.objects.get(id=new_recipe.id)
		for step in steps:
			Step.objects.create(
				instruction=step['instruction'], order=step['order'],
				required_time=step['required_time'], recipe=recipe_object
				)
		return new_recipe