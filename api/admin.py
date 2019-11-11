from django.contrib import admin
from .models import Course, Cuisine, Ingredient, Image, Meal, Profile, Recipe, Step


class IngredientAdmin(admin.ModelAdmin):
	list_display = ('name', 'category', 'id')


class ProfileAdmin(admin.ModelAdmin):
	list_display = ('id', 'user', 'gender', 'phone', 'date_of_birth')
	readonly_fields = ('name', 'email')
	list_display_links = ('id', 'user')

	def name(self, obj):
		return obj.user.get_full_name()
	
	def email(self,obj): 
		return obj.user.email


class StepInline(admin.TabularInline):
	model = Step
	extra = 1


class ImageInLine(admin.TabularInline):
	model = Image
	extra = 1


class RecipeAdmin(admin.ModelAdmin):
	list_display = ('id','title','cuisine','total_time')
	list_display_links = ('id', 'title')
	list_filter = ('cuisine', 'courses', 'meals')
	inlines = (
		StepInline,
		ImageInLine
	)


admin.site.register(Course)
admin.site.register(Cuisine)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Meal)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Recipe, RecipeAdmin)