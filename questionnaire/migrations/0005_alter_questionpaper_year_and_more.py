# Generated by Django 4.2.14 on 2024-08-02 08:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questionnaire', '0004_questionpaper_year_of_study_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questionpaper',
            name='year',
            field=models.IntegerField(default=2024),
        ),
        migrations.AlterField(
            model_name='questionpaper',
            name='year_of_study',
            field=models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')], default='1', max_length=2),
        ),
    ]
