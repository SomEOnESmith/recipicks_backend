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
	)
	name = models.CharField(max_length=100)
	category = models.CharField(choices=CATEGORY, max_length=20, null=True, blank=True)
	color = models.CharField(max_length=20, null=True, blank=True)

	def __str__(self):
		return self.name

@receiver(post_save, sender=Ingredient)
@receiver(post_delete, sender=Ingredient)
def create_color(sender, instance, created,**kwargs):
	if created:
		if (instance.category == "Protein"):
			instance.color = "red"
		elif (instance.category == "Vegetable"):
			instance.color = "green"
		elif (instance.category == "Fruit"): 
			instance.color = "orange"
		elif (instance.category == "Dairy"):
			instance.color = "white"
		elif (instance.category == "Grain"):
			instance.color = "blue"
		elif (instance.category == "Bean"):
			instance.color = "yellow"
		else:
			instance.color =="purple"
		instance.save()
# def get_readonly_fields(self, request, obj=None):
#     if obj:
#         return self.readonly_fields + ('person',)
#     return self.readonly_fields


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
	total_time = models.DurationField(default='00:00:00')

	def __str__(self):
		return self.title

	def get_total_time(self):
		self.total_time = sum(self.steps.values_list('required_time', flat=True), timedelta())
		self.save()


class Step(models.Model):
	instruction = models.TextField()
	order = models.PositiveIntegerField(blank=True, null=True)
	required_time = models.DurationField()
	recipe = models.ForeignKey(Recipe, related_name="steps", on_delete=models.CASCADE)
	
	class Meta:
		ordering = ['order',]

	def __str__(self):
		return self.recipe.title

@receiver(post_save, sender=Step)
@receiver(post_delete, sender=Step)
def update_recipe(sender, instance, **kwargs):
	instance.recipe.get_total_time()


class Profile(models.Model):
	GENDER = (
		("Female", "Female"),
		("Male", "Male")
	)
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	phone = models.PositiveIntegerField(blank=True, null=True)
	gender = models.CharField(choices=GENDER, max_length=6, null=True, blank=True)
	date_of_birth = models.DateField(blank=True, null=True)
	image = models.ImageField(null=True, blank=True)
	liked_recipes =  models.ManyToManyField(Recipe, blank=True, related_name="liked_recipes")
	disliked_recipes = models.ManyToManyField(Recipe, blank=True, related_name="disliked_recipes")

	def __str__(self):
		return self.user.username

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(user=instance)
