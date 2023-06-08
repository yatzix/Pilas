from django.urls import path
from . import views

urlpatterns = [
		path('', views.home, name='home'),
		path('about/', views.about, name='about'),
        path('week/<int:pk>/', views.WeekDetailView.as_view(), name='week_detail'),
        path('week/<int:pk>/day/<int:day_id>/', views.DayDetailView.as_view(), name='day_detail'),
        path('week/<int:pk>/day/<int:day_id>/search/', views.RecipeSearchView.as_view(), name='recipe_search'),
        path('accounts/signup/', views.signup, name='signup',)
]