# Generated by Django 2.2.3 on 2019-08-07 16:20

from django.db import migrations, models
from project.models import PublishedProject

def featured(apps, schema_editor):
    projects = PublishedProject.objects.filter()

    i = 1
    for p in projects:
        if p.featured == 0:
            p.featured = None
        else:
            p.featured = i
            i += 1

        p.save()

        
class Migration(migrations.Migration):

    dependencies = [
        ('project', '0029_publishedproject_display_publications'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publishedproject',
            name='featured',
            field=models.PositiveSmallIntegerField(null=True),
        ),
        migrations.RunPython(featured),
        migrations.AlterUniqueTogether(
            name='publishedproject',
            unique_together={('featured',), ('core_project', 'version')},
        ),
    ]