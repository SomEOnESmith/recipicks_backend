from django.db import models


class Ingredient(models.Model):
	name = models.CharField(max_length=100)

	def __str__(self):
		return self.name


class MealType(models.Model):
	name = models.CharField(max_length=100)

	def __str__(self):
		return self.name


class MealTime(models.Model):
	name = models.CharField(max_length=100)

	def __str__(self):
		return self.name


class Cuisine(models.Model):
	name = models.CharField(max_length=100)

	def __str__(self):
		return self.name


class Recipe(models.Model):
	title = models.CharField(max_length=100)
	description = models.TextField()
	image = models.ImageField(blank=True)
	steps = models.TextField(blank=True)
	ingredients = models.ManyToManyField(Ingredient, related_name="recipe")
	meal_type = models.ManyToManyField(MealType, related_name="recipe")
	meal_time = models.ManyToManyField(MealTime, related_name="recipe")
	required_time = models.DurationField()
	cuisine = models.ForeignKey(Cuisine, null=True, related_name="recipe", on_delete=models.SET_NULL)

	class Meta:
		verbose_name_plural = "recipies"

	def __str__(self):
		return self.title