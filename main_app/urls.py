from django.urls import path
from . import views

urlpatterns = [
		path('', views.home, name='home'),
		path('about/', views.about, name='about'),
        path('week/', views.week_index, name='index'),
        path('week/create/', views.WeekCreate.as_view(), name='week_create'),
        path('week/<int:pk>/update/', views.WeekUpdate.as_view(), name='week_update'),
        path('week/<int:pk>/delete/', views.WeekDelete.as_view(), name='week_delete'),
        path('days/create/<int:week_id>', views.DayCreate.as_view(), name='days_create'),
        path('days/<int:pk>/update/', views.DayUpdate.as_view(), name='days_update'),
        path('days/<int:pk>/delete/', views.DayDelete.as_view(), name='days_delete'),
        path('week/<int:pk>/', views.WeekDetailView.as_view(), name='week_detail'),
        path('week/<int:pk>/day/<int:day_id>/recipe/<int:recipe_id>/', views.DayDetailView.as_view(), name='day_detail'),
        path('week/<int:pk>/day/<int:day_id>/', views.DayDetailView.as_view(), name='day_detail'),
        path('week/<int:pk>/day/<int:day_id>/search/', views.RecipeSearchView.as_view(), name='recipe_search'),
        path('week/<int:week_id>/day/<int:day_id>/recipe/<int:recipe_id>/save/', views.save_recipe, name='save_recipe'),
        path('week/<int:week_id>/day/<int:day_id>/recipe/save/', views.save_recipe, name='save_recipe'),
        path('accounts/signup/', views.signup, name='signup',)
]

