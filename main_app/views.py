from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import requests
from django.urls import reverse
from django.contrib.auth import login
from django.views import View
from .models import Week, Day, Recipe
from django.views.decorators.http import require_POST


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

def week_index(request):
    weeks = Week.objects.filter(user=request.user)
    return render(request, 'index.html', {'weeks': weeks})

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
        week = self.object.week
        day = self.object 
        recipes = Recipe.objects.filter(day=day)
        saved_recipes = Recipe.objects.filter(day=day)

        context['week'] = week
        context['recipes'] = recipes
        context['saved_recipes'] = saved_recipes
        return context

    def get_object(self):
        week_id = self.kwargs.get('pk')
        day_id = self.kwargs.get('day_id')
        
        return self.model.objects.get(week__id=week_id, id=day_id)
        



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

        for recipe in recipes:
            recipe['recipe_id'] = recipe['idMeal']

        print(api_data)  
        print(recipes)  

        context = {
            'week': week,
            'day': day,
            'query': query,
            'recipes': recipes,
            
        }

        return render(request, 'day_detail.html', context)

@require_POST
def save_recipe(request, week_id, day_id, recipe_id):

    name = request.POST.get('name')
    instructions = request.POST.get('instructions')
    thumbnail = request.POST.get('thumbnail')
    ingredients = request.POST.get('ingredients')
    video_link = request.POST.get('video_link')
    source_link = request.POST.get('source_link')
    day = Day.objects.get(id=day_id)


    recipe = Recipe(
        name=name, 
        instructions=instructions,
        thumbnail=thumbnail,
        ingredients=ingredients,
        video_link=video_link,
        source_link=source_link,
        day=day
    )
    recipe.save()

    return redirect('day_detail', pk=week_id, day_id=day_id, recipe_id=recipe_id)


    


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

class WeekCreate(LoginRequiredMixin,CreateView):
    model = Week
    fields = ['name']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class WeekList(LoginRequiredMixin,ListView):
    model = Week


class WeekUpdate(LoginRequiredMixin,UpdateView):
    model = Week
    fields = ['name']

class WeekDelete(LoginRequiredMixin,DeleteView):
    model = Week
    success_url = '/week/'

class DayCreate(LoginRequiredMixin,CreateView):
    model = Day
    fields = ['name']

    def form_valid(self, form):
        week = Week.objects.get(pk=self.kwargs['week_id'])
        form.instance.week = week
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('week_detail', kwargs={'pk': self.object.week.pk})
    

class DayList(LoginRequiredMixin,ListView):
    model = Day


class DayUpdate(LoginRequiredMixin,UpdateView):
    model = Day
    fields = ['name']

    def get_success_url(self):
        return reverse('week_detail', kwargs={'pk': self.object.week.pk})

class DayDelete(LoginRequiredMixin,DeleteView):
    model = Day
    success_url = '/week/'

