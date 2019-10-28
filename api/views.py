from rest_framework.generics import (
	CreateAPIView, ListAPIView, RetrieveAPIView, RetrieveUpdateAPIView
	)
from .serializers import (
	UserCreateSerializer, CreateUpdateProfileSerializer,
	RecipeDetailsSerializer, RecipesListSerializer
	 )
from .models import Recipe, Profile
from rest_framework.permissions import IsAuthenticated


class UserCreateAPIView(CreateAPIView):
	serializer_class = UserCreateSerializer


class ProfileView(RetrieveUpdateAPIView):
	serializer_class = CreateUpdateProfileSerializer
	permission_classes = [IsAuthenticated]

	def get_object(self):
		return Profile.objects.get(user=self.request.user)


class RecipeListView(ListAPIView):
	queryset = Recipe.objects.all()
	serializer_class = RecipesListSerializer
 

class RecipeDetailsView(RetrieveAPIView):
	queryset = Recipe.objects.all()
	serializer_class = RecipeDetailsSerializer
	lookup_field = 'id'
	lookup_url_kwarg = 'recipe_id'
