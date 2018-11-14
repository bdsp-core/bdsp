"""
Command to:
- load all fixtures named 'demo-*.*'
- create copy the demo media files

This should only be called in a clean database, such as after
`resetdb` is run. This should generally only be used in
development environments.

"""
import os
import shutil

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand

from physionet.utility import get_project_apps


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

        project_apps = get_project_apps()
        demo_fixtures = find_demo_fixtures(project_apps)

        call_command('loaddata', *demo_fixtures, verbosity=1)

        # Copy the demo project and user media content
        for content in ['users', 'active-projects', 'published-projects',
                        'credential-applications']:
            copy_demo_media(content)


def find_demo_fixtures(project_apps):
    """
    Find non-empty demo fixtures
    """
    demo_fixtures = []
    for app in project_apps:
        fixture = 'demo-{}'.format(app)
        file_name = os.path.join(settings.BASE_DIR, app,
                                 'fixtures', '{}.json'.format(fixture))
        if os.path.exists(file_name) and open(file_name).read(4) != '[\n]\n':
            demo_fixtures.append(fixture)

    return demo_fixtures


def copy_demo_media(subdir):
    "Copy the demo content from the specified subdirectory"
    demo_subdir = os.path.join(settings.MEDIA_ROOT, 'demo', subdir)
    target_subdir = os.path.join(settings.MEDIA_ROOT, subdir)

    for item in os.listdir(demo_subdir):
        shutil.copytree(os.path.join(demo_subdir, item),
                        os.path.join(target_subdir, item))
