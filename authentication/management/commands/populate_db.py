from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import Group
from meta.models import MetaData, DownloadLink


class Command(BaseCommand):
    help = 'Populates initial data to the DB. This command must be run once after setup.'

    def handle(self, *args, **options):

        try:
            print('Creating Permission Groups')
            Group.objects.get_or_create(name='Faculty')
            Group.objects.get_or_create(name='Student')
            self.stdout.write(self.style.SUCCESS(
                'Created permission group Faculty and Student. Please add appropriate permission to the groups in admin panel.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(
                f'Failed to create groups. Error {e}'))

        try:
            MetaData.objects.get_or_create(
                min_app_build=6,
                min_app_version='1.2.1',
            )
            self.stdout.write(self.style.SUCCESS(
                'Added application version metadata.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(
                f'Failed to add MetaData. Error {e}.'))

        try:

            DownloadLink.objects.get_or_create(
                apk_download='https://fase.thecodepapaya.dev',
                ios_download='https://fase.thecodepapaya.dev',
            )
            self.stdout.write(self.style.SUCCESS(
                f'Added default download links.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(
                f'Failed to add download links. Error {e}.'))

        self.stdout.write(self.style.SUCCESS('Success'))
