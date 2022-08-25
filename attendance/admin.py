from django.contrib import admin

# Register your models here.
from attendance.models import User, Lecturer, Student, Class, Course, CollegeDay, Semester

admin.site.register(User)
admin.site.register(Lecturer)
admin.site.register(Student)
admin.site.register(Class)
admin.site.register(Course)
admin.site.register(CollegeDay)
admin.site.register(Semester)