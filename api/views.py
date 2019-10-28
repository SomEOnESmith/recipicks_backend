from rest_framework.generics import (ListAPIView, RetrieveAPIView)
from .serializers import (RecipeDetailsSerializer, RecipesListSerializer)
from .models import Recipe



class RecipeListView(ListAPIView):
	queryset = Recipe.objects.all()
	serializer_class = RecipesListSerializer

class RecipeDetailsView(RetrieveAPIView):
	queryset = Recipe.objects.all()
	serializer_class = RecipeDetailsSerializer
	lookup_field = 'id'
	lookup_url_kwarg = 'recipe_id'



