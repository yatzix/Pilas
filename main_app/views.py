from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import DaysOfTheWeek, Recipe
import requests
from django.contrib.auth import login
import environ

# Create your views here.
from django.shortcuts import render

def home(request):
	  return render(request, 'home.html')
def about(request):
	  return render(request, 'about.html')

@login_required
def daysOftheWeek(request):
  daysOftheWeek = DaysOfTheWeek.objects.filter(user=request.user)
  return render(request, 'daysOftheWeek/index.html', {'daysOftheWeek': daysOftheWeek})

@login_required
def daysOfTheWeek_detail(request, dayOfTheWeek_id):
  daysOfTheWeek = DaysOfTheWeek.objects.get(id=dayOfTheWeek_id)
  id_list = daysOfTheWeek.recipes.all().values_list('id') 
  recipes_user_doesnt_have = Recipe.objects.exclude(id__in=id_list)
  return render(request, 'dayOfTheWeek/detail.html', { 'dayOfTheWeek': daysOfTheWeek, 'recipes': recipes_user_doesnt_have})


class RecipeDetail(LoginRequiredMixin,DetailView):
    model = Recipe

LoginRequiredMixin,
def signup(request):
    # POST request menas user is signing up with a form submission
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
        else:
            error_message = 'invalid signup - try again'
    form = UserCreationForm()
    return render(request, 'registration/signup.html', {
        'form': form,
        'error': error_message
    })


def recipes(request):
    api_url = 'https://api.calorieninjas.com/v1/recipe?query='
    query = 'mushroom risotto'
    env = environ.Env()
    api_key = env('API_KEY')
    response = requests.get(api_url + query, headers={'X-Api-Key': 'YOUR_API_KEY'})
    if response.status_code == requests.codes.ok:
        print(response.text)
    else:
        print("Error:", response.status_code, response.text)
