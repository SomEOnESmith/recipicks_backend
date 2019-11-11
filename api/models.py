from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from datetime import timedelta


class Ingredient(models.Model):
	CATEGORY = (
		("Protein", "Protein"),
		("Vegetable", "Vegetable"),
		("Fruit", "Fruit"),
		("Dairy", "Dairy"),
		("Grain", "Grain"),
		("Bean", "Bean"),
		("Nut", "Nut"),
		("Others", "Others"),

	)
	name = models.CharField(max_length=100)
	category = models.CharField(choices=CATEGORY, default="Others", max_length=20)

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
	image = models.ImageField()
	courses = models.ManyToManyField("Course", related_name="recipes")
	cuisine = models.ForeignKey("Cuisine", null=True, related_name="recipes", on_delete=models.SET_NULL)
	ingredients = models.ManyToManyField("Ingredient", related_name="recipes")
	meals = models.ManyToManyField("Meal", related_name="recipes")
	total_time = models.DurationField(null=True, blank=True)

	def __str__(self):
		return self.title

	def get_total_time(self):
		self.total_time = sum(self.steps.values_list("required_time", flat=True), timedelta())
		self.save()


class Step(models.Model):
	instruction = models.TextField()
	order = models.PositiveIntegerField(default=0)
	required_time = models.DurationField()
	recipe = models.ForeignKey("Recipe", related_name="steps", on_delete=models.CASCADE)
	
	class Meta:
		ordering = ['order',]

	def __str__(self):
		return self.recipe.title

@receiver(post_save, sender=Step)
@receiver(post_delete, sender=Step)
def update_recipe(sender, instance, **kwargs):
	instance.recipe.get_total_time()


class Image(models.Model):
	image = models.ImageField()
	recipe = models.ForeignKey("Recipe", related_name="images", on_delete=models.CASCADE)


class Profile(models.Model):
	GENDER = (
		("Female", "Female"),
		("Male", "Male")
	)
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	date_of_birth = models.DateField(null=True)
	gender = models.CharField(choices=GENDER, max_length=6, null=True, blank=True)
	image = models.ImageField(null=True, blank=True)
	phone = models.PositiveIntegerField(null=True)
	liked_recipes =  models.ManyToManyField("Recipe", blank=True, related_name="liked_recipes")
	disliked_recipes = models.ManyToManyField("Recipe", blank=True, related_name="disliked_recipes")

	def __str__(self):
		return self.user.username

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(user=instance)