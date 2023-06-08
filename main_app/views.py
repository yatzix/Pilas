from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import requests
from django.contrib.auth import login
from environ import Env
from django.views import View
from .models import Week, Day, Recipe

def home(request):
    weeks = Week.objects.all()
    days = Day.objects.all()
    context = {
        'weeks': weeks,
        'days': days,
    }
    return render(request, 'home.html', context)

def about(request):
    return render(request, 'about.html')

class WeekDetailView(DetailView):
    model = Week
    template_name = 'week_detail.html'
    context_object_name = 'week'

class DayDetailView(LoginRequiredMixin, DetailView):
    model = Day
    template_name = 'day_detail.html'
    context_object_name = 'day'
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Retrieve the associated Week object
        week = self.object.week
        # Add the Week object to the context
        context['week'] = week
        return context


class RecipeSearchView(LoginRequiredMixin, View):
    def get(self, request, pk, day_id):
        week = Week.objects.get(pk=pk)
        day = Day.objects.get(pk=day_id)
        query = request.GET.get('query', '')

        url = "https://www.themealdb.com/api/json/v1/1/search.php"
        querystring = {"s": query}
        response = requests.get(url, params=querystring)

        if response.status_code == requests.codes.ok:
            api_data = response.json()
            recipes = api_data.get('meals', [])
        else:
            recipes = []

        print(api_data)  # Print the API response for debugging
        print(recipes)  # Print the extracted recipes for debugging

        context = {
            'week': week,
            'day': day,
            'query': query,
            'recipes': recipes,
        }

        return render(request, 'day_detail.html', context)






def signup(request):
    error_message = ''
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
