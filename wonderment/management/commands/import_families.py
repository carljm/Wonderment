from django.core.management import BaseCommand

from wonderment import import_data, models


class Command(BaseCommand):
    def handle(self, *args, **options):
        session = models.Session.objects.get(pk=args[1])
        return import_data.import_csv(session, args[0])
