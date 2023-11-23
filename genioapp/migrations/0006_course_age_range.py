# Generated by Django 4.2.7 on 2023-11-23 23:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('genioapp', '0005_studentorder_completion_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='age_range',
            field=models.CharField(choices=[('1', '(7-11)'), ('2', '(12-14)'), ('3', '(15-17)'), ('4', '(17+)')], default='1', max_length=10),
        ),
    ]
