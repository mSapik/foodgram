import csv

from django.core.management.base import BaseCommand

from recipes.models import Ingredient

FILE = 'data/ingredients.csv'


class Command(BaseCommand):
    """Импорт данных из CSV."""

    def handle(self, *args, **options):
        print(f'Началась загрузка файла {FILE}')
        try:
            rows = []
            with open(
                FILE, 'r',
                encoding='utf8', newline=''
            ) as file:
                reader = csv.reader(file)
                for row in reader:
                    name, measurement_unit = row
                    rows.append(Ingredient(name=name,
                                           measurement_unit=measurement_unit))
            Ingredient.objects.bulk_create(rows)
            print(self.style.SUCCESS(f'Файл {FILE} УСПЕШНО загружен'))
        except FileNotFoundError:
            print(self.style.ERROR(f'Ошибка: Файл {FILE} не найден'))
        except Exception as e:
            print(self.style.ERROR(
                f'Ошибка при загрузке файла {FILE}: {e}'))
