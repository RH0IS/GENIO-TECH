# Generated by Django 4.2.7 on 2023-11-17 14:24

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("genioapp", "0002_course_image_course_video_instructor_image_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="instructor",
            name="country",
        ),
    ]