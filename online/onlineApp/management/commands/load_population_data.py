from django.core.management.base import BaseCommand
from onlineApp.models import Population
import csv


class Command(BaseCommand):
    help = "Loads population data from CSV file."

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to CSV file')

    def handle(self, *args, **options):
        csv_file_path = options['csv_file']
        try:
            with open(csv_file_path, 'r') as file:
                reader = csv.reader(file)
                next(reader)  # skips header row
                for row in reader:
                    continent, year, population_value = row
                    Population.objects.create(continent=continent, year=int(
                        year), population=population_value
                    )
                    self.stdout.write(self.style.SUCCESS(
                        f'Successfully loaded data from "{csv_file_path}"'))
        except FileNotFoundError:
            self.stderr.write(self.style.ERROR(
                f'File not found"{csv_file_path}"'))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Error loading data: "{e}"'))
