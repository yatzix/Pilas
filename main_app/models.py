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
    
    def get_absolute_url(self):
        return reverse('week_detail', kwargs={'pk': self.pk})
    
class Day(models.Model):
    week = models.ForeignKey(Week, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name    
    def get_absolute_url(self):
        return reverse('day_detail', kwargs={'pk': self.pk})

class Recipe(models.Model):
    idMeal = models.CharField(max_length=10, null=True,)
    name = models.CharField(max_length=300)
    thumbnail = models.URLField(default='') 
    instructions = models.TextField(default='')
    ingredients = models.TextField(default='')
    video_link = models.URLField(default='')
    source_link = models.URLField(default='')
    day = models.ForeignKey('Day', null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
