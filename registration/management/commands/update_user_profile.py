from django.core.management.base import BaseCommand

from registration.models import UserProfile


class Command(BaseCommand):
    help = 'Update profile of user'

    def handle(self, *args, **options):
        pass
