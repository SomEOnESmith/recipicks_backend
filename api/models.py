from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver 


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

	def __str__(self):
		return self.title
#fix time to signal post save
	def get_total_time(self):
		return sum([time for time in self.steps.required_time])


class Step(models.Model):
	instruction = models.TextField()
	required_time = models.DurationField()
	recipe = models.ForeignKey(Recipe, related_name="steps", on_delete=models.CASCADE)

	
	def __str__(self):
		return self.recipe.title



class Profile(models.Model):
	GENDER = (
		("Female", "Female"),
		("Male", "Male")
	)
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
	phone = models.PositiveIntegerField(null=True, blank=True)
	gender = models.CharField(choices=GENDER, max_length=6, null=True, blank=True)
	date_of_birth = models.DateField(null=True, blank=True)
	image = models.ImageField(null=True, blank=True)
	liked_recipes =  models.ManyToManyField(Recipe, null=True, blank=True, related_name="liked_recipes")
	disliked_recipes = models.ManyToManyField(Recipe, null=True, blank=True, related_name="disliked_recipes")

	def __str__(self):
		return self.user.username

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
