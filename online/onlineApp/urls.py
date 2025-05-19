from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('populations/', views.population_list, name='population_list'),
    path('populations/<int:pk>/', views.population_detail,
         name='population_detail'),  # Corrected line
    path('population_plot/', views.population_plot_view, name='population_plot'),
    path('continent_detail/', views.continent_detail_view, name='continent_detail'),
]
# calls function in views.py so it can be seen in browser
