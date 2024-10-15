from barcode_app.models import LabelSpecification
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.management import BaseCommand, call_command


class Command(BaseCommand):
    def handle(self, *args, **options):
        call_command("makemigrations")
        call_command("migrate")
        User.objects.filter(email="admin@example.com").delete()
        User.objects.create_superuser(
            "admin", email="admin@example.com", password="admin"  # nosec B106
        )
        try:
            LabelSpecification.objects.get(name="default")
        except ObjectDoesNotExist:
            LabelSpecification.objects.create()
            print("Created default label specification.")
        else:
            print("Default label specification already exists.")
        print("Created a default user `admin` with password `admin`")
