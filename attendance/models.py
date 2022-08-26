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
    # One semester runs one to many courses
    # One course is run in zero to many semesters
    course = models.ManyToManyField(Course, related_name='semester_course', blank=False)

    def __str__(self):
        return self.id.__str__()


class CollegeDay(models.Model):
    date = models.DateField(primary_key=True)

    def __str__(self):
        return self.date.__str__()


class Class(models.Model):
    number = models.IntegerField(primary_key=True)
    # One course can be separated into one to many classes
    # One class can only run for one course
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='class_course', blank=False)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    # One class can be taught by only one lecturer,
    # One lecturer teaches zero to many classes
    lecturer = models.ForeignKey(Lecturer, on_delete=models.CASCADE, blank=False)
    # One class holds one to many students’ enrollments
    # One student fit in one class
    student = models.ForeignKey(Student, on_delete=models.CASCADE, blank=False)
    # One college day runs zero to many classes
    # One class runs on zero to many college days
    collegeDay = models.ManyToManyField(CollegeDay, related_name='class_collegeDay', blank=True)

    def __str__(self):
        return self.number.__str__()

