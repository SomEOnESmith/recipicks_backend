from rest_framework import serializers
from drf_writable_nested import WritableNestedModelSerializer
from django.contrib.auth.models import User

from .models import Profile, Recipe, Cuisine, Ingredient, Course, Meal, Step, Image


class UserCreateSerializer(serializers.ModelSerializer):
	password = serializers.CharField(write_only=True)
	class Meta:
		model = User
		fields = ['username', 'password']

	def create(self, validated_data):
		new_user = User(**validated_data)
		new_user.set_password(validated_data['password'])
		new_user.save()
		return validated_data


class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ("username", "first_name", "last_name", "email")
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


class CuisineSerializer(serializers.ModelSerializer):
	class Meta:
		model = Cuisine
		fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
	class Meta:
		model = Course
		fields = '__all__'


class MealSerializer(serializers.ModelSerializer):
	class Meta:
		model = Meal
		fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):
	class Meta:
		model = Ingredient
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
	# images = ImageSerializer(many=True)

	class Meta:
		model = Recipe
		exclude = ('total_time','image')


class RecipeListSerializer(serializers.ModelSerializer):
	meals = MealSerializer(many=True)
	cuisine = CuisineSerializer()

	class Meta:
		model = Recipe
		exclude = ('description', 'courses')