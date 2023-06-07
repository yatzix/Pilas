from django.urls import path
from . import views

urlpatterns = [
		path('', views.home, name='home'),
		path('about/', views.about, name='about'),
        path('daysOfTheWeek/<int:daysOfTheWeek_id>/', views.daysOfTheWeek_detail, name='detail'),
        path('recipes/<int:pk>/', views.RecipeDetail.as_view(), name='recipe_detail'),
        path('accounts/signup/', views.signup, name='signup',)
]