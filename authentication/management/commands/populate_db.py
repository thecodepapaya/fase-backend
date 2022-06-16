from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import Group
from meta.models import MetaData


class Command(BaseCommand):
    help = 'Populates initial data to the DB. This command must be run once after setup.'

    def handle(self, *args, **options):

        print('Creating Permission Groups')
        faculty_group = Group.objects.get_or_create(name='Faculty')
        student_group = Group.objects.get_or_create(name='Student')

        meta_data = MetaData.objects.create(
            min_app_build=6,
            min_app_version='1.2.1',
        )

        self.stdout.write(self.style.SUCCESS('Success'))
