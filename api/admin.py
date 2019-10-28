from django.contrib import admin
from .models import (Recipe, Ingredient, Cuisine, Course, Meal, Step)

class RecipeAdmin(admin.ModelAdmin):
	list_display = ('title',)

admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient)
admin.site.register(Cuisine)
admin.site.register(Course)
admin.site.register(Meal)
admin.site.register(Step)
