# Generated by Django 4.2.14 on 2024-08-13 06:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questionnaire', '0006_questionpaper_intake'),
    ]

    operations = [
        migrations.AddField(
            model_name='faculty',
            name='icon',
            field=models.ImageField(blank=True, null=True, upload_to='icons/'),
        ),
    ]
