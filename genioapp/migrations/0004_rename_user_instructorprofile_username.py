# Generated by Django 4.2.6 on 2023-11-16 23:01

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("genioapp", "0003_instructorprofile"),
    ]

    operations = [
        migrations.RenameField(
            model_name="instructorprofile",
            old_name="user",
            new_name="username",
        ),
    ]