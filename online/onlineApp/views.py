from .models import Population
from django.template import loader
from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
import os
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Agg")


# Agg is headless backend, create and render w/o interacting with GUI


def index(request):
    # point to the app specific inner directory
    specific_year = 2020  # latest year data available
    latest_populations = Population.objects.filter(year=specific_year)

    context = {'latest_populations': latest_populations}
    # template = loader.get_template('onlineApp/index.html')
    # print(context)
    # loads specific template and renders w/context data
    return render(request, 'onlineApp/index.html', context)


def get_continent_choices():
    """Gets the unique list of continents from the database."""
    return Population.objects.values_list('continent', flat=True).distinct().order_by('continent')


def plot_continent_population(continent_data, save_path, continent_name):
    plt.figure(figsize=(10, 6))
    years = [item['year'] for item in continent_data]
    populations = [item['population'] for item in continent_data]
    plt.plot(years, populations, marker='+')
    plt.title(f"Population of {continent_name} Over Time")
    plt.xlabel("Year")
    plt.ylabel("Population")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()


def continent_detail_view(request):
    continents = get_continent_choices()
    selected_continent = request.GET.get('continent')
    plot_url = None

    if selected_continent:
        continent_data = Population.objects.filter(
            continent=selected_continent).order_by('year').values('year', 'population')

        if continent_data:
            static_path = os.path.join(settings.STATIC_ROOT, 'images')
            os.makedirs(static_path, exist_ok=True)
            image_filename = f"{selected_continent.lower().replace(' ', '_')}.population.png"
            image_path = os.path.join(static_path, image_filename)
            image_url = os.path.join(
                settings.STATIC_URL, 'images', image_filename)

            plot_continent_population(
                list(continent_data), image_path, selected_continent)

    context = {'continents': continents,
               'selected_continent': selected_continent, 'plot_url': plot_url}
    return render(request, 'onlineApp/population_detail.html', context)


def online_population_from_db():
    population_by_continent = {}
    # fetches all Population objects from database, orders by continent and year
    populations = Population.objects.all().order_by('continent', 'year')

    for pop in populations:
        continent = pop.continent
        year = pop.year
        population = pop.population

        if continent not in population_by_continent:
            population_by_continent[continent] = {
                'years': [], 'population': []}
        population_by_continent[continent]['years'].append(year)
        population_by_continent[continent]['population'].append(population)

    return population_by_continent


def plot_population_by_continent(population_by_continent, save_path):
    plt.figure(figsize=(10, 6))
    for continent in population_by_continent:
        years = population_by_continent[continent]['years']
        population_continent = (
            population_by_continent[continent]['population'])
        plt.plot(years, population_continent,
                 label=continent, alpha=0.5, marker='+')
    plt.title("Online Population by Continent")
    plt.xlabel("Year")
    plt.ylabel("Population")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()


def population_plot_view(request):
    # call to get data from the database
    population_data = online_population_from_db()
    static_path = os.path.join(settings.STATICFILES_DIRS[0], 'images')
    os.makedirs(static_path, exist_ok=True)
    image_path = os.path.join(static_path, 'population_plot.png')
    image_url = os.path.join(
        settings.STATIC_URL, 'images', 'population_plot.png')
    plot_population_by_continent(population_data, image_path)
    context = {'plot_url': image_url}
    return render(request, 'onlineApp/population_plot.html', context)


def population_list(request):
    """  Displays a list of all entries """
    populations = Population.objects.all()  # retrieves all data from Population table
    context = {
        'populations': populations
    }
    return render(request, 'onlineApp/index.html', context)


def population_detail(request, pk):
    """ Displays the details of a specific population"""
    try:
        # retrieves single recordwith the given primary key
        population = Population.objects.get(pk=pk)
        context = {
            'population': population
        }
        return render(request, 'onlineApp/population_detail.html', context)

    except Population.DoesNotExist:
        return render(request, 'onlineApp/population_not_found.html', {
            'population_id': pk}, status=404)
