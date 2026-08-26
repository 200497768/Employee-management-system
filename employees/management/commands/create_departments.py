from django.core.management.base import BaseCommand

from employees.departments import Departments



class Command(BaseCommand):
    help = "Creates departments"

    def handle(self, *args, **options)->None:
        departments:Departments=Departments()
        departments.create()

        self.stdout.write(self.style.SUCCESS('Departments created.'))