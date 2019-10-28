from django.db import models


class Ingredient(models.Model):
	name = models.CharField(max_length=100)

	def __str__(self):
		return self.name


class Course(models.Model):
	name = models.CharField(max_length=100)

	def __str__(self):
		return self.name


class Meal(models.Model):
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
	ingredients = models.ManyToManyField(Ingredient, related_name="recipes")
	course = models.ManyToManyField(Course, related_name="recipes")
	meal = models.ManyToManyField(Meal, related_name="recipes")
	cuisine = models.ForeignKey(Cuisine, null=True, related_name="recipes", on_delete=models.SET_NULL)

	class Meta:
		verbose_name_plural = "recipies"

	def __str__(self):
		return self.title

	def get_total_time(self):
		return sum([time for time in self.steps.required_time])


class Step(models.Model):
	instruction = models.TextField()
	required_time = models.DurationField()
	recipe = models.ForeignKey(Recipe, related_name="steps", on_delete=models.CASCADE)
