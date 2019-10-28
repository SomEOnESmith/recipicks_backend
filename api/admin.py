from django.contrib import admin
from .models import Recipe, Ingredient, Cuisine, MealType, MealTime

class RecipeAdmin(admin.ModelAdmin):
	list_display = ('title', 'required_time')

admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient)
admin.site.register(Cuisine)
admin.site.register(MealType)
admin.site.register(MealTime)
