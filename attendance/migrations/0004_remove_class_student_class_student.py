# Generated by Django 4.1 on 2022-09-30 07:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("attendance", "0003_course_hours_per_day"),
    ]

    operations = [
        migrations.RemoveField(model_name="class", name="student",),
        migrations.AddField(
            model_name="class",
            name="student",
            field=models.ManyToManyField(
                related_name="class_student", to="attendance.student"
            ),
        ),
    ]