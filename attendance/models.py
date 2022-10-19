from django.db import models
from django.contrib.auth.models import User

# Create your models here.


# class User(models.Model):
#     id = models.IntegerField(primary_key=True)
#     first_name = models.CharField(max_length=30, null=True, blank=True)
#     last_name = models.CharField(max_length=30, null=True, blank=True)
#     email = models.CharField(max_length=200, null=True, blank=True)
#
#     def __str__(self):
#         return self.id.__str__()


class Lecturer(models.Model):
    staff_id = models.IntegerField()
    DOB = models.DateField(null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.staff_id.__str__()


class Student(models.Model):
    student_id = models.IntegerField()
    DOB = models.DateField(null=False)
    # 10.One student enrollment belongs to one student.
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.student_id.__str__()


class Course(models.Model):
    id = models.IntegerField(primary_key=True)
    code = models.CharField(max_length=200, null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    hours_per_day = models.IntegerField(blank=False)
    totalhours = models.IntegerField(blank=False)

    def __str__(self):
        return self.id.__str__()


class Semester(models.Model):
    id = models.IntegerField(primary_key=True)
    year = models.IntegerField()
    semester = models.CharField(max_length=200, null=True, blank=True)
    # 1.One semester runs one to many courses
    # 2.One course is run in zero to many semesters
    course = models.ManyToManyField(Course, related_name='semester_course', blank=True)

    def __str__(self):
        return self.id.__str__()


class Class(models.Model):
    id = models.IntegerField(primary_key=True)
    number = models.IntegerField()
    # 3.One course can be separated into one to many classes
    # 4.One class can only run for one course
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='class_course', blank=False)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    # 5.One class can be taught by only one lecturer,
    # 6.One lecturer teaches zero to many classes
    lecturer = models.ForeignKey(Lecturer, on_delete=models.CASCADE, blank=True)
    # 7.One class holds one to many students’ enrollments
    # 8.One enrollment fit in one class
    student = models.ManyToManyField(Student, related_name='class_student', blank=False)

    def __str__(self):
        return self.number.__str__()


class Attendance(models.Model):
    id = models.IntegerField(primary_key=True)
    # need to remove object when removing student, course, or class
    student = models.ForeignKey(Student, on_delete=models.CASCADE, blank=False)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, blank=False)
    classes = models.ForeignKey(Class, on_delete=models.CASCADE, blank=False)
    absent_hours = models.IntegerField(blank=False)
    attendance_rate = models.FloatField(blank=False)

    def __str__(self):
        return self.id.__str__()


class CollegeDay(models.Model):
    id = models.IntegerField(primary_key=True, blank=False)
    date = models.DateField()
    # 11.One college day runs zero to many classes
    # 12.One class runs on zero to many college days
    Class = models.ManyToManyField(Class, blank=True, related_name="collegeday_class")

    def __str__(self):
        return self.date.__str__()




