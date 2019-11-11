from django.contrib import admin
from .models import (Recipe, Profile, Ingredient, Cuisine, Course, Meal, Step,Ingredient, Image)

class StepInline(admin.TabularInline):
	model = Step
	extra = 1


class ImageInLine(admin.TabularInline):
	model = Image
	extra = 1


class RecipeAdmin(admin.ModelAdmin):
	list_display = ('id','title','cuisine','total_time')
	list_display_links = ('id', 'title')
	inlines = (
		StepInline,
		ImageInLine
	)


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Profile)
admin.site.register(Ingredient)
admin.site.register(Cuisine)
admin.site.register(Course)
admin.site.register(Meal)
admin.site.register(Step)
