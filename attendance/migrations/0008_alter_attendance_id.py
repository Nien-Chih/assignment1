# Generated by Django 4.1 on 2022-10-09 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "attendance",
            "0007_remove_attendance_course_remove_attendance_student_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="attendance",
            name="id",
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]
