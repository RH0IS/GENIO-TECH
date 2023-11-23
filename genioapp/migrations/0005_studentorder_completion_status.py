# Generated by Django 4.2.7 on 2023-11-23 22:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('genioapp', '0004_alter_studentorder_unique_together'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentorder',
            name='completion_status',
            field=models.CharField(choices=[('completed', 'Completed'), ('ongoing', 'On-going')], default='On-going', max_length=10),
        ),
    ]
