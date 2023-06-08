from os import name
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.

class Week(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
class Day(models.Model):
    week = models.ForeignKey(Week, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name    

class Recipe(models.Model):
    name = models.CharField(max_length=100)
    servings = models.IntegerField()
    ingredients = models.CharField(max_length=1000)
    instructions = models.TextField(max_length=750)

    def __str__(self):
        return self.name
