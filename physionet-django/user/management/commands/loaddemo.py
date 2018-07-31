"""
Command to:
- load all fixtures named 'demo-*.*'
- create symbolic links of demo projects to projects directory

This should only be called in a clean database, such as after
`resetdb` is run. This should generally only be used in
development environments.

"""
import os

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):
        # If not in development, prompt warning messages twice
        if 'development' not in os.environ['DJANGO_SETTINGS_MODULE']:
            warning_messages = ['You are NOT in the development environment. Are you sure you want to insert demo data? [y/n]',
                                'The demo data will be mixed with existing data. Are you sure? [y/n]',
                                'Final warning. Are you ABSOLUTELY SURE? [y/n]']
            for i in range(3):
                choice = input(warning_messages[i]).lower()
                if choice != 'y':
                    sys.exit('Exiting from load. No actions applied.')
            print('Continuing loading demo data')

        project_apps = ['user', 'project']
        demo_fixtures = ['demo-' + app for app in project_apps]

        # Remove data from all tables. Tables are kept.
        call_command('loaddata', *demo_fixtures, verbosity=1)

        # Link the demo project folders
        projects_dir = os.path.join(settings.MEDIA_ROOT, 'project')
        demo_projects_dir = os.path.join(settings.MEDIA_ROOT, 'demo', 'project')
        for item in os.listdir(demo_projects_dir):
            os.symlink(os.path.join(demo_projects_dir, item), os.path.join(projects_dir, item))
