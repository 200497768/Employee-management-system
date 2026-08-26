from django.core.management.base import BaseCommand

from employees.offices import Offices


class Command(BaseCommand):
    help = "Creates offices"

    def handle(self, *args, **options)->None:
        offices:Offices=Offices()
        offices.create()

        self.stdout.write(self.style.SUCCESS('Offices created.'))