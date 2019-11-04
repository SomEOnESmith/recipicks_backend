from django.contrib import admin
from .models import (Recipe, Profile, Ingredient, Cuisine, Course, Meal, Step,Ingredient)

class StepInline(admin.TabularInline):
	model = Step
	extra = 1


class RecipeAdmin(admin.ModelAdmin):
	list_display = ('title',)
	inlines = [
		StepInline,
	]

class IngredientAdmin(admin.ModelAdmin):
	model = Ingredient
	readonly_fields = ('color', )

admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Profile)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Cuisine)
admin.site.register(Course)
admin.site.register(Meal)
admin.site.register(Step)
