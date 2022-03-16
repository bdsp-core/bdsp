# Generated by Django 2.2.24 on 2021-12-15 13:59
import os

from django.conf import settings
from django.core.management import call_command

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
from django.db.models.fields import DurationField

from project.modelcomponents.fields import SafeHTMLField
from user.enums import TrainingStatus, RequiredField
from user.models import get_training_path, training_report_path
from user.validators import validate_alphaplusplus


def migrate_forward(apps, schema_editor):
    call_command('loaddata', os.path.join(settings.BASE_DIR, 'user', 'fixtures', 'demo-training-type.json'))

    Training = apps.get_model('user', 'Training')
    TrainingType = apps.get_model('user', 'TrainingType')
    TrainingQuestion = apps.get_model('user', 'TrainingQuestion')
    CredentialApplication = apps.get_model('user', 'CredentialApplication')

    training_type = TrainingType.objects.first()

    status_mapping = {
        0: TrainingStatus.REVIEW,
        1: TrainingStatus.REJECTED,
        2: TrainingStatus.ACCEPTED,
        3: TrainingStatus.WITHDRAWN,
        4: TrainingStatus.REJECTED
    }

    for credential_application in CredentialApplication.objects.all():
        report_url = (
            ""
            if credential_application.training_completion_report_url is None
            else credential_application.training_completion_report_url
        )

        training = Training.objects.create(
            slug=credential_application.slug,
            training_type=training_type,
            user=credential_application.user,
            completion_report=credential_application.training_completion_report,
            completion_report_url=report_url,
            application_datetime=credential_application.training_completion_date,
            process_datetime=credential_application.decision_datetime,
            status=status_mapping[credential_application.status],
        )

        training_questions = []
        for question in training.training_type.questions.all():
            training_questions.append(TrainingQuestion(training=training, question=question))

        TrainingQuestion.objects.bulk_create(training_questions)


def migrate_backward(apps, schema_editor):
    ...


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0034_user_sso_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='Training',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(max_length=20, unique=True)),
                (
                    'status',
                    models.PositiveSmallIntegerField(
                        choices=[(0, 'REVIEW'), (1, 'WITHDRAWN'), (2, 'REJECTED'), (3, 'ACCEPTED')],
                        default=TrainingStatus(0),
                    ),
                ),
                (
                    'completion_report',
                    models.FileField(
                        blank=True,
                        upload_to=get_training_path,
                        validators=[django.core.validators.FileExtensionValidator(['pdf'], 'File must be a pdf.')],
                    ),
                ),
                ('completion_report_url', models.URLField(blank=True)),
                ('application_datetime', models.DateTimeField(auto_now_add=True)),
                ('process_datetime', models.DateTimeField(null=True)),
                ('reviewer_comments', models.CharField(max_length=512)),
                (
                    'reviewer',
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name='reviewed_training',
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name='TrainingType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('home_page', models.URLField(blank=True)),
                ('description', SafeHTMLField()),
                ('valid_duration', DurationField(null=True)),
                (
                    'required_field',
                    models.PositiveSmallIntegerField(
                        choices=[(0, 'DOCUMENT'), (1, 'URL')], default=RequiredField(0)
                    ),
                ),
                ('questions', models.ManyToManyField(related_name='training_types', to='user.Question')),
            ],
        ),
        migrations.CreateModel(
            name='TrainingQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.NullBooleanField()),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.Question')),
                (
                    'training',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='training_questions',
                        to='user.Training',
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name='training',
            name='training_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.TrainingType'),
        ),
        migrations.AddField(
            model_name='training',
            name='user',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, related_name='training', to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AlterField(
            model_name='credentialapplication',
            name='training_completion_report',
            field=models.FileField(
                upload_to=training_report_path,
                null=True,
                validators=[django.core.validators.FileExtensionValidator(['pdf'], 'File must be a pdf.')]
            )
        ),
        migrations.AlterField(
            model_name='credentialapplication',
            name='training_course_name',
            field=models.CharField(
                max_length=100,
                null=True,
                validators=[validate_alphaplusplus]
            )
        ),
        migrations.RunPython(migrate_forward, migrate_backward),
    ]
