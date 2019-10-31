from rest_framework.generics import (
	CreateAPIView, ListAPIView, RetrieveAPIView, RetrieveUpdateAPIView,
)
from rest_framework.views import APIView

from .serializers import (
	UserCreateSerializer, CreateUpdateProfileSerializer,
	RecipeDetailsSerializer, RecipesListSerializer, IngredientSerializer
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

#wrong ListCreateAPIView 
class RecipesByIngredientListView(APIView):
	serializer_class = RecipesListSerializer
	def post(self,request):
		print(request.data)




	# def get_queryset(self):
	# 	# Step 1: need to loop through the list of recived ingredients using request.data

	# 	# Step 2: need to make condition for the filtering example:
	# 	"""
	# 	contition = 
	# 	return Recipe.objects.filter(ingredient__name= request.data.ingredient[0] && ingredient__name= request.data.ingredient[1])

	# 	"""
		# return Recipe.objects.all()





