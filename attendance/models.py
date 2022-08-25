from django.db import models

# Create your models here.


class User(models.Model):
    id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=30, null=True, blank=True)
    last_name = models.CharField(max_length=30, null=True, blank=True)
    email = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.id.__str__()


class Lecturer(models.Model):
    staff_id = models.IntegerField(primary_key=True)
    DOB = models.DateField(null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.staff_id.__str__()


class Student(models.Model):
    student_id = models.IntegerField(primary_key=True)
    DOB = models.DateField(null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.student_id.__str__()


class Course(models.Model):
    id = models.IntegerField(primary_key=True)
    code = models.CharField(max_length=200, null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.id.__str__()


class Semester(models.Model):
    id = models.IntegerField(primary_key=True)
    year = models.IntegerField()
    semester = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return  self.id.__str__()


class Class(models.Model):
    number = models.IntegerField(primary_key=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    lecturer = models.ForeignKey(Lecturer, on_delete=models.CASCADE)

    def __str__(self):
        return self.number.__str__()


class CollegeDay(models.Model):
    date = models.DateField(primary_key=True)

    def __str__(self):
        return self.date.__str__()

