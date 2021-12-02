# Generated by Django 2.2.6 on 2020-02-22 00:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0048_remove_fixed_content_fields'),
    ]

    operations = [
        migrations.AddField(
            model_name='activesectioncontent',
            name='custom_order',
            field=models.PositiveSmallIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='activesectioncontent',
            name='custom_title',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='archivedsectioncontent',
            name='custom_order',
            field=models.PositiveSmallIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='archivedsectioncontent',
            name='custom_title',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='publishedsectioncontent',
            name='custom_order',
            field=models.PositiveSmallIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='publishedsectioncontent',
            name='custom_title',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='activesectioncontent',
            name='project_section',
            field=models.ForeignKey(
                db_column='project_section', null=True, on_delete=django.db.models.deletion.PROTECT,
                related_name='activesectioncontents', to='project.ProjectSection'),
        ),
        migrations.AlterField(
            model_name='archivedsectioncontent',
            name='project_section',
            field=models.ForeignKey(
                db_column='project_section', null=True, on_delete=django.db.models.deletion.PROTECT,
                related_name='archivedsectioncontents', to='project.ProjectSection'),
        ),
        migrations.AlterField(
            model_name='publishedsectioncontent',
            name='project_section',
            field=models.ForeignKey(
                db_column='project_section', null=True, on_delete=django.db.models.deletion.PROTECT,
                related_name='publishedsectioncontents', to='project.ProjectSection'),
        ),
    ]
