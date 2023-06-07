from os import name
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.
class Recipe(models.Model):
    name = models.CharField(max_length=100)
    servings = models.IntegerField()
    ingredients = models.CharField(max_length=1000)
    instructions = models.TextField(max_length=750)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('detail', kwargs={'recipe_id': self.id})
    
    
class DaysOfTheWeek(models.Model):
    name = models.CharField(max_length=100)

    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)


class Week(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dayOfTheWeek = models.ForeignKey(DaysOfTheWeek, on_delete=models.CASCADE)