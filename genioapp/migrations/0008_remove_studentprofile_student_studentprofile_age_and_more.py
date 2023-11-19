# Generated by Django 4.2.7 on 2023-11-18 23:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('genioapp', '0007_remove_course_students_remove_instructor_students_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='studentprofile',
            name='student',
        ),
        migrations.AddField(
            model_name='studentprofile',
            name='age',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='studentprofile',
            name='country',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='studentprofile',
            name='email',
            field=models.EmailField(default='w@example.com', max_length=254, unique=True),
        ),
        migrations.AddField(
            model_name='studentprofile',
            name='gender',
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AddField(
            model_name='studentprofile',
            name='name',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='studentprofile',
            name='phone',
            field=models.CharField(blank=True, max_length=15),
        ),
    ]
