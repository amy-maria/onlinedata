from django.db import models

# Create your models here.


class Population(models.Model):
    continent = models.CharField(max_length=255)
    year = models.IntegerField()
    population = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.continent} - {self.year}: {self.population}"
