# Generated by Django 4.2.7 on 2023-11-24 00:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('genioapp', '0006_course_age_range'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='age_range',
            field=models.CharField(choices=[('(7-11)', '(7-11)'), ('(12-14)', '(12-14)'), ('(15-17)', '(15-17)'), ('(17+)', '(17+)')], default='1', max_length=10),
        ),
    ]
