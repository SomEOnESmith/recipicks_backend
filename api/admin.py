from django.contrib import admin
from .models import (Recipe, Profile, Ingredient, Cuisine, Course, Meal, Step)

class StepInline(admin.TabularInline):
	model = Step
	extra = 1


class RecipeAdmin(admin.ModelAdmin):
	list_display = ('title',)
	inlines = [
		StepInline,
	]

admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Profile)
admin.site.register(Ingredient)
admin.site.register(Cuisine)
admin.site.register(Course)
admin.site.register(Meal)
admin.site.register(Step)
