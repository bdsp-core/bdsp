import os
from subprocess import call
from django.core.management import execute_from_command_line
from physionet import settings
from user.models import User, Profile

from django.core import management
from django.core.management.commands import loaddata
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):

    def handle(self, *args, **options):
        installed_apps = [a for a in settings.INSTALLED_APPS if 'django' not in a]
        self.deletedb(installed_apps)
        user0,user1,user2 = self.createusers(installed_apps)
        self.loadfixtures(installed_apps)
        self.adduserprofiles(user0,user1,user2)

    def remove_migration_files(self,app):
        '''Remove all python migration files from registered apps'''
        app_migrations_dir = os.path.join(settings.BASE_DIR, app, 'migrations')
        if os.path.isdir(app_migrations_dir):
            migration_files = [file for file in os.listdir(app_migrations_dir) if file.startswith('0') and file.endswith('.py')]
            for file in migration_files:
                os.remove(os.path.join(app_migrations_dir, file))

    def deletedb(self,installed_apps):
        """
        Delete the database and associated files
        """
        for app in installed_apps:
            self.remove_migration_files(app)

        # delete the database
        fn = 'db.sqlite3'
        try:
            os.remove(os.path.join(settings.BASE_DIR, fn))
        except:
            pass

        # Remake and reapply the migrations
        execute_from_command_line(['manage.py', 'makemigrations'])
        execute_from_command_line(['manage.py', 'migrate'])

    def createusers(self,installed_apps):
        """
        Create some demo users
        """
        user0 = User.objects.create_superuser(email="tester@mit.edu", password="Tester1!")
        user1 = User.objects.create_user(email="rgmark@mit.edu", password="Tester1!")
        user2 = User.objects.create_user(email="george@mit.edu", password="Tester1!")

        return user0,user1,user2


    def loadfixtures(self,installed_apps):
        """
        Insert the demo content from the fixtures files
        """ 
        for app in installed_apps:
            app_fixtures_dir = os.path.join(settings.BASE_DIR, app, 'fixtures')
            management.call_command('loaddata', app, verbosity=1)


    def adduserprofiles(self,user0,user1,user2):
        """
        Add user profiles
        """
        user0.profile = Profile.objects.get(first_name='Tester')
        user0.save()

        user1.profile = Profile.objects.get(first_name='Roger Greenwood')
        user1.save()

        user2.profile = Profile.objects.get(first_name='George')
        user2.save()