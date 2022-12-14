# Generated by Django 4.1 on 2022-09-16 02:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Class",
            fields=[
                ("id", models.IntegerField(primary_key=True, serialize=False)),
                ("number", models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="Course",
            fields=[
                ("id", models.IntegerField(primary_key=True, serialize=False)),
                ("code", models.CharField(blank=True, max_length=200, null=True)),
                ("name", models.CharField(blank=True, max_length=200, null=True)),
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
                ("student_id", models.IntegerField()),
                ("DOB", models.DateField()),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Semester",
            fields=[
                ("id", models.IntegerField(primary_key=True, serialize=False)),
                ("year", models.IntegerField()),
                ("semester", models.CharField(blank=True, max_length=200, null=True)),
                (
                    "course",
                    models.ManyToManyField(
                        blank=True,
                        related_name="semester_course",
                        to="attendance.course",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Lecturer",
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
                ("staff_id", models.IntegerField()),
                ("DOB", models.DateField()),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="CollegeDay",
            fields=[
                ("id", models.IntegerField(primary_key=True, serialize=False)),
                ("date", models.DateField()),
                (
                    "Class",
                    models.ManyToManyField(
                        blank=True,
                        related_name="collegeday_class",
                        to="attendance.class",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="class",
            name="course",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="class_course",
                to="attendance.course",
            ),
        ),
        migrations.AddField(
            model_name="class",
            name="lecturer",
            field=models.ForeignKey(
                blank=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="attendance.lecturer",
            ),
        ),
        migrations.AddField(
            model_name="class",
            name="semester",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="attendance.semester"
            ),
        ),
        migrations.AddField(
            model_name="class",
            name="student",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="attendance.student"
            ),
        ),
    ]
