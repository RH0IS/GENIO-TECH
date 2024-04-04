# Generated by Django 5.0.3 on 2024-04-04 02:55

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="ClassRoom",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(default="user", max_length=200)),
                ("uid", models.CharField(default="0", max_length=1000)),
                ("room_name", models.CharField(default="classroom", max_length=200)),
                (
                    "user_role",
                    models.CharField(default="Student", max_length=200, null=True),
                ),
                ("insession", models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name="Course",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=200, null=True)),
                ("description", models.TextField(null=True)),
                ("start_date", models.TextField(null=True)),
                ("end_date", models.TextField(null=True)),
                (
                    "price",
                    models.DecimalField(decimal_places=2, max_digits=10, null=True),
                ),
                ("interested", models.PositiveIntegerField(default=0, null=True)),
                (
                    "age_range",
                    models.CharField(
                        choices=[
                            ("(7-11)", "(7-11)"),
                            ("(12-14)", "(12-14)"),
                            ("(15-17)", "(15-17)"),
                            ("(17+)", "(17+)"),
                        ],
                        default="1",
                        max_length=10,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="CourseLevels",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                (
                    "price",
                    models.DecimalField(
                        decimal_places=2, default=25, max_digits=10, null=True
                    ),
                ),
                ("description", models.CharField(max_length=100)),
                (
                    "course",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="genioapp.course",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="CourseSession",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "session",
                    models.IntegerField(
                        choices=[
                            (1, "Session 1"),
                            (2, "Session 2"),
                            (3, "Session 3"),
                            (4, "Session 4"),
                        ]
                    ),
                ),
                ("start_datetime", models.CharField(blank=True, max_length=50)),
                ("end_datetime", models.CharField(blank=True, max_length=50)),
                (
                    "class_room",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="genioapp.classroom",
                    ),
                ),
                (
                    "course_level",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="genioapp.courselevels",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="InstructorProfile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "first_name",
                    models.CharField(default="first_name", max_length=100, null=True),
                ),
                ("last_name", models.CharField(max_length=100, null=True)),
                (
                    "email",
                    models.EmailField(
                        default=None, max_length=254, null=True, unique=True
                    ),
                ),
                ("bio", models.TextField(null=True)),
                (
                    "language",
                    models.CharField(default="none", max_length=100, null=True),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="course",
            name="instructor",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="genioapp.instructorprofile",
            ),
        ),
        migrations.CreateModel(
            name="IntructorAvailability",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("day", models.DateField(default=django.utils.timezone.now)),
                ("start_time", models.TimeField(default="08:00")),
                ("end_time", models.TimeField(default="09:00")),
                ("available", models.BooleanField(default=False)),
                (
                    "instructor",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="genioapp.instructorprofile",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Student",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(blank=True, max_length=50)),
                (
                    "email",
                    models.EmailField(
                        default="w@example.com", max_length=254, unique=True
                    ),
                ),
                ("age", models.IntegerField(blank=True, null=True)),
                ("gender", models.CharField(blank=True, max_length=10)),
                ("phone", models.CharField(blank=True, max_length=15)),
                ("country", models.CharField(blank=True, max_length=50)),
                (
                    "user",
                    models.OneToOneField(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Order",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "order_status",
                    models.IntegerField(
                        choices=[(0, "Order Confirmed"), (1, "Order Cancelled")],
                        default=1,
                    ),
                ),
                ("order_date", models.DateField()),
                ("order_price", models.DecimalField(decimal_places=2, max_digits=10)),
                ("levels", models.PositiveIntegerField()),
                (
                    "course",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="genioapp.course",
                    ),
                ),
                (
                    "student",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="genioapp.student",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="StudentProfile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(blank=True, max_length=50)),
                (
                    "email",
                    models.EmailField(
                        default="w@example.com", max_length=254, unique=True
                    ),
                ),
                ("age", models.IntegerField(blank=True, null=True)),
                ("gender", models.CharField(blank=True, max_length=10)),
                ("phone", models.CharField(blank=True, max_length=15)),
                ("country", models.CharField(blank=True, max_length=50)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="StudentOrder",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "completion_status",
                    models.CharField(
                        choices=[("completed", "Completed"), ("ongoing", "On-going")],
                        default="On-going",
                        max_length=10,
                    ),
                ),
                (
                    "course_level",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="genioapp.courselevels",
                    ),
                ),
                (
                    "student",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="genioapp.studentprofile",
                    ),
                ),
            ],
            options={
                "unique_together": {("student", "course_level")},
            },
        ),
    ]
