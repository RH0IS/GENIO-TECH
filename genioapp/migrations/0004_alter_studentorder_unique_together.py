# Generated by Django 4.2.7 on 2023-11-23 17:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('genioapp', '0003_studentorder'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='studentorder',
            unique_together={('student', 'course_level')},
        ),
    ]
