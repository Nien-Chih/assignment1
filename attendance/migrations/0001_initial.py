# Generated by Django 4.1 on 2022-08-25 08:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="CollegeDay",
            fields=[("date", models.DateField(primary_key=True, serialize=False)),],
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
            name="Semester",
            fields=[
                ("id", models.IntegerField(primary_key=True, serialize=False)),
                ("year", models.IntegerField()),
                ("semester", models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="User",
            fields=[
                ("id", models.IntegerField(primary_key=True, serialize=False)),
                ("first_name", models.CharField(blank=True, max_length=30, null=True)),
                ("last_name", models.CharField(blank=True, max_length=30, null=True)),
                ("email", models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Student",
            fields=[
                ("student_id", models.IntegerField(primary_key=True, serialize=False)),
                ("DOB", models.DateField()),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="attendance.user",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Lecturer",
            fields=[
                ("staff_id", models.IntegerField(primary_key=True, serialize=False)),
                ("DOB", models.DateField()),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="attendance.user",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Class",
            fields=[
                ("number", models.IntegerField(primary_key=True, serialize=False)),
                (
                    "course",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="attendance.course",
                    ),
                ),
                (
                    "lecturer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="attendance.lecturer",
                    ),
                ),
                (
                    "semester",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="attendance.semester",
                    ),
                ),
            ],
        ),
    ]
