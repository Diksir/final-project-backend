# Generated by Django 4.2.14 on 2024-07-29 13:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('questionnaire', '0002_questionpaper_content_qsession_message'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='credits',
        ),
        migrations.RemoveField(
            model_name='course',
            name='description',
        ),
        migrations.RemoveField(
            model_name='faculty',
            name='department',
        ),
        migrations.RemoveField(
            model_name='faculty',
            name='email',
        ),
        migrations.RemoveField(
            model_name='faculty',
            name='office_address',
        ),
        migrations.RemoveField(
            model_name='faculty',
            name='phone',
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('faculty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='departments', to='questionnaire.faculty')),
            ],
        ),
        migrations.AddField(
            model_name='course',
            name='department',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='courses', to='questionnaire.department'),
            preserve_default=False,
        ),
    ]
