from django.contrib import admin
from .models import Population

# Register your models here.
# create new class to define list labels for admin table


class PopulationAdmin(admin.ModelAdmin):
    list_display = ("continent", "year", "population")


admin.site.register(Population, PopulationAdmin)
