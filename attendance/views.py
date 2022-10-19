import json
import datetime

from django.contrib.auth.models import Group
from django.core.files.storage import FileSystemStorage
from django.core.mail import send_mail
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth import authenticate, login
from attendance.forms import RegistrationForm
from attendance.models import Semester, Course, Class, Lecturer, User, Student, Attendance
import pandas as pd


# Create your views here.
def index(request):
    return render(request, "index.html")


def Login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        # Redirect to a success page.
    else:
        # Return an 'invalid login' error message.
        ...
    return render(request, "registration/login.html")


def getSemesterByCourseId(request, course_id):
    course = Course.objects.get(id=course_id)
    tmep = set()
    semesters = course.semester_course.all()
    for semester in semesters:
        tmep.add(semester.semester)
    resp = list(tmep)
    resp.sort()
    return HttpResponse(json.dumps(resp))


def semester(request):
    semesters = Semester.objects.all()
    courses = Course.objects.all()
    context = {"semester_all": semesters, "course_all": courses}
    return render(request, "semester.html", context)


def semesterDetail(request, semester_id):
    semester = Semester.objects.get(id=semester_id)
    context = {"semester": semester}
    return render(request, "semesterdetail.html", context)


def createSemester(request):
    semester_year = request.POST.get("semester_year")
    semester_semester = request.POST.get("semester_semester")
    semester_course = request.POST.get("semester_course")
    semester_all = Semester.objects.all()
    semester = Semester.objects.create(id=len(semester_all) + 1, semester=semester_semester, year=semester_year)
    course = Course.objects.get(id=semester_course)
    semester.course.add(course)
    semester.save()
    return HttpResponseRedirect(reverse('get-semester'))


def updateSemester(request):
    semester_id = request.POST.get("semester_id")
    semester_year = request.POST.get("semester_year")
    semester_semester = request.POST.get("semester_semester")
    semester = Semester.objects.get(id=semester_id)
    semester.year = semester_year
    semester.semester = semester_semester
    semester.save()
    return HttpResponseRedirect(reverse("get-semester"))


def deleteSemester(request, semester_id):
    semester = Semester.objects.get(id=semester_id)
    semester.delete()
    return HttpResponseRedirect(reverse("get-semester"))


# course course course course course course course course
def course(request):
    courses = Course.objects.all()
    context = {"course_all": courses}
    return render(request, "course.html", context)


def courseDetail(request, course_id):
    course = Course.objects.get(id=course_id)
    context = {"course": course}
    return render(request, "coursedetail.html", context)


def createCourse(request):
    course_name = request.POST.get("course_name")
    course_code = request.POST.get("course_code")
    course_hours_per_day = request.POST.get("course_hours_per_day")
    course_total_hours = request.POST.get("course_total_hours")
    course = Course(name=course_name, code=course_code, hours_per_day=course_hours_per_day,
                    totalhours=course_total_hours)
    course.save()
    return HttpResponseRedirect(reverse('get-course'))


def updateCourse(request):
    course_id = request.POST.get("course_id")
    course_name = request.POST.get("course_name")
    course_code = request.POST.get("course_code")
    course = Course.objects.get(id=course_id)
    course.name = course_name
    course.code = course_code
    course.save()
    return HttpResponseRedirect(reverse("get-course"))


def deleteCourse(request, course_id):
    course = Course.objects.get(id=course_id)
    course.delete()
    return HttpResponseRedirect(reverse("get-course"))


# classes classes classes classes classes classes classes
def classes(request):
    classes = Class.objects.all()
    course = Course.objects.all()
    semester = Semester.objects.all()
    lecturer = Lecturer.objects.all()
    students = Student.objects.all()
    context = {"classes_all": classes, "course_all": course, "semester_all": semester, "lecturer_all": lecturer,
               "student_all": students}
    return render(request, "classes.html", context)


def classesDetail(request, classes_id):
    classes = Class.objects.get(id=classes_id)
    course_all = Course.objects.all()
    semester_all = Semester.objects.all()
    lecturer_all = Lecturer.objects.all()
    classes.course.semester_course.all()
    student_all = Student.objects.all()
    context = {"classes": classes, "course_all": course_all, "semester_all": semester_all, "lecturer_all": lecturer_all,
               "student_all": student_all}
    return render(request, "classesdetail.html", context)


def createClasses(request):
    classes_number = request.POST.get("class_number")
    classes_course_id = request.POST.get("class_course_id")
    classes_semester_id = request.POST.get("class_semester_id")
    classes_lecturer_id = request.POST.get("class_lecturer_staff_id")
    # classes_student_id = request.POST.get("class_student_id")
    course = Course.objects.get(id=classes_course_id)
    semester = Semester.objects.get(id=classes_semester_id)
    lecturer = Lecturer.objects.get(staff_id=classes_lecturer_id)
    # student = Student.objects.get(student_id=classes_student_id)
    attendStudents = request.POST.getlist('AttendStudents')
    student_all = Student.objects.all()
    classes_all = Class.objects.all()
    classes = Class.objects.create(id=len(classes_all) + 1, number=classes_number, course=course, semester=semester,
                                   lecturer=lecturer)
    for student in student_all:
        if str(student.student_id) in attendStudents:
            classes.student.add(student)
    classes.save()
    for student in classes.student.all():
        Attendance.objects.create(student=student, course=course, classes=classes, absent_hours=0, attendance_rate=1.0)
    return HttpResponseRedirect(reverse('get-classes'))


def updateClasses(request):
    classes_id = request.POST.get("classes_id")
    classes_number = request.POST.get("class_number")
    classes_course_id = request.POST.get("class_course_id")
    classes_semester_id = request.POST.get("class_semester_id")
    classes_lecturer_staff_id = request.POST.get("class_lecturer_staff_id")
    # classes_student_id = request.POST.get("class_student_id")
    course = Course.objects.get(id=classes_course_id)
    semester = Semester.objects.get(id=classes_semester_id)
    lecturer = Lecturer.objects.get(staff_id=classes_lecturer_staff_id)
    classes = Class.objects.get(id=classes_id)
    # student = Student.objects.get(student_id=classes_student_id)
    attendStudents = request.POST.getlist('AttendStudents')
    student_all = Student.objects.all()
    classes.number = classes_number
    classes.course = course
    classes.semester = semester
    classes.lecturer = lecturer
    # classes.student = student
    for student in student_all:
        if str(student.student_id) in attendStudents:
            classes.student.add(student)
    classes.save()
    return HttpResponseRedirect(reverse("get-classes"))


def deleteClasses(request, classes_id):
    classes = Class.objects.get(id=classes_id)
    classes.delete()
    return HttpResponseRedirect(reverse("get-classes"))


# lecturer lecturer lecturer lecturer lecturer lecturer
def lecturer(request):
    lectures = Lecturer.objects.all()
    context = {"lecturer_all": lectures}
    return render(request, "lecturer.html", context)


def lecturerDetail(request, staff_id):
    lecturer = Lecturer.objects.get(staff_id=staff_id)
    context = {"lecturer": lecturer}
    return render(request, "lecturerdetail.html", context)


def createLecturer(request):
    lecturer_fname = request.POST.get("lecturer_fname")
    lecturer_lname = request.POST.get("lecturer_lname")
    lecturer_DOB = request.POST.get("lecturer_DOB")
    lecturer_email = request.POST.get("lecturer_email")
    dob = str(lecturer_DOB).split(" ")[0].replace("-", "")
    user = User.objects.create_user(username=lecturer_fname.lower() + lecturer_lname.lower())
    user.first_name = lecturer_fname
    user.last_name = lecturer_lname
    user.email = lecturer_email
    user.set_password(dob)
    try:
        group = Group.objects.get(name='Lecturer')
        user.groups.add(group)
    except Group.DoesNotExist:
        group = Group.objects.create(name='Lecturer')
        group.save()
        user.groups.add(group)
    user.save()
    lecturer = Lecturer.objects.create(staff_id=user.id, DOB=lecturer_DOB, user=user)
    lecturer.save()
    return HttpResponseRedirect(reverse('get-lecturer'))


def updateLecturer(request):
    staff_id = request.POST.get("staff_id")
    lecturer_fname = request.POST.get("lecturer_fname")
    lecturer_lname = request.POST.get("lecturer_lname")
    lecturer_DOB = request.POST.get("lecturer_DOB")
    dob = str(lecturer_DOB).split(" ")[0].replace("-", "")
    lecturer = Lecturer.objects.get(staff_id=staff_id)
    user = User.objects.get(id=lecturer.user.id)
    user.first_name = lecturer_fname
    user.last_name = lecturer_lname
    user.set_password(dob)
    user.save()
    lecturer.DOB = lecturer_DOB
    lecturer.save()
    return HttpResponseRedirect(reverse("get-lecturer"))


def deleteLecturer(request, staff_id):
    lecturer = Lecturer.objects.get(staff_id=staff_id)
    user = User.objects.get(id=lecturer.user.id)
    lecturer.delete()
    user.delete()
    return HttpResponseRedirect(reverse("get-lecturer"))


def lecturerAttendance(request, staff_id):
    lecturer = Lecturer.objects.get(staff_id=staff_id)
    class_all = Class.objects.filter(lecturer=lecturer)
    context = {"class_all": class_all}
    return render(request, "lecturerattendance.html", context)


def attendanceCourses(request):
    class_all = Class.objects.all()
    context = {"class_all": class_all}
    return render(request, "attendancecourse.html", context)


def lecturerAttendanceDetail(request, class_id):
    classes = Class.objects.get(id=class_id)
    attendance_all = Attendance.objects.filter(course=classes.course)
    date = datetime.datetime.now()
    context = {"classes": classes, "Date": date, "attendance_all": attendance_all}
    return render(request, "lecturerattendancedetail.html", context)


def saveAttendance(request):
    class_id = request.POST.get("class_id")
    classes = Class.objects.get(id=class_id)
    course = Course.objects.get(id=classes.course.id)
    absent_student_ids = list(map(int, request.POST.getlist("absent_student_ids")))
    students = classes.student.all()
    for student in students:
        if student.student_id in absent_student_ids:
            attendance = Attendance.objects.filter(student=student, course=course, classes=classes)
            if len(attendance) == 0:
                print("attendance not found")
            else:
                attendance[0].absent_hours += classes.course.hours_per_day
                attendance[0].attendance_rate = (classes.course.totalhours - attendance[
                    0].absent_hours) / classes.course.totalhours
                attendance[0].save()
        else:
            print("student not found")
    return HttpResponseRedirect(reverse('lecturer-attendance', kwargs={'staff_id': classes.lecturer.staff_id}))


# student student student student student student

def student(request):
    students = Student.objects.all()
    context = {"student_all": students}
    return render(request, "student.html", context)


def studentDetail(request, student_id):
    student = Student.objects.get(student_id=student_id)
    context = {"student": student}
    return render(request, "studentdetail.html", context)


def createStudent(request):
    student_fname = request.POST.get("student_fname")
    student_lname = request.POST.get("student_lname")
    student_DOB = request.POST.get("student_DOB")
    student_email = request.POST.get("student_email")
    dob = str(student_DOB).split(" ")[0].replace("-", "")
    user = User.objects.create_user(username=student_fname.lower() + student_lname.lower())
    user.first_name = student_fname
    user.last_name = student_lname
    user.email = student_email
    user.set_password(dob)
    try:
        group = Group.objects.get(name='Student')
        user.groups.add(group)
    except Group.DoesNotExist:
        group = Group.objects.create(name='Student')
        group.save()
        user.groups.add(group)
    user.save()
    student = Student.objects.create(student_id=user.id, DOB=student_DOB, user=user)
    student.save()
    return HttpResponseRedirect(reverse('get-student'))


def updateStudent(request):
    student_id = request.POST.get("student_id")
    student_fname = request.POST.get("student_fname")
    student_lname = request.POST.get("student_lname")
    student_DOB = request.POST.get("student_DOB")
    student = Student.objects.get(student_id=student_id)
    student.DOB = student_DOB
    dob = str(student_DOB).split(" ")[0].replace("_", "")
    user = User.objects.get(id=student.user.id)
    user.first_name = student_fname
    user.last_name = student_lname
    user.set_password(dob)
    user.save()
    student.save()
    return HttpResponseRedirect(reverse("get-student"))


def deleteStudent(request, student_id):
    student = Student.objects.get(student_id=student_id)
    user = User.objects.get(id=student.user.id)
    user.delete()
    student.delete()
    return HttpResponseRedirect(reverse("get-student"))


def file_upload(request):
    if request.method == "POST" and request.FILES["myfile"]:
        myfile = request.FILES["myfile"]
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        upload_file_url = fs.url(filename)
        excel_data = pd.read_excel(myfile)
        data = pd.DataFrame(excel_data)
        usernames = data["Username"].tolist()
        firstnames = data["First Name"].tolist()
        lastnames = data["Last Name"].tolist()
        emails = data["Email"].tolist()
        dobs = data["DOB"].tolist()
        i = 0
        while i < len(usernames):
            username = usernames[i]
            try:
                User.objects.get(username=username)
                i = i + 1
                continue
            except User.DoesNotExist:
                filename = firstnames[i]
                lastname = lastnames[i]
                email = emails[i]
                dob = str(dobs[i]).split(" ")[0].replace("_", "")
                user = User(username=username)
                user.first_name = filename
                user.last_name = lastname
                user.email = email
                user.set_password(dob)
                user.groups.add(1)
                user.save()
                student_all = Student.objects.all()
                student = Student.objects.create(student_id=user.id, DOB=dob, user=user)
                student.save()
                i = i + 1
        return HttpResponseRedirect(reverse("get-student"))
    return HttpResponseRedirect(reverse("get-student"))


class RegistrationView(CreateView):
    model = User
    template_name = 'registration/register.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('login')


def CustomRegistration(request):
    if request.method == "POST":
        username = request.POST.get("username")
        firstname = request.POST.get("firstname")
        lastname = request.POST.get("lastname")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        if password1 == password2:
            user = User.objects.create_user(username=username)
            user.first_name = firstname
            user.last_name = lastname
            user.email = email
            user.set_password(password1)
            user.save()
            return HttpResponseRedirect(request("login"))
        else:
            return render(request, "registration_success.html", {"message": "Password are not same"})

    return render(request, "registration_success.html")


def studentClasses(request):
    classes_all = Class.objects.all()
    context = {"classes_all": classes_all}
    return render(request, "studentclasses.html", context)


def studentClassesDetail(request, class_id):
    classes = Class.objects.get(id=class_id)
    context = {"class": classes}
    return render(request, "studentsclassesdetail.html", context)


def deleteStudentClass(request, class_id, student_id):
    classes = Class.objects.get(id=class_id)
    student = Student.objects.get(student_id=student_id)
    classes.student.remove(student.id)
    Attendance.objects.filter(student=student, course=classes.course, classes=classes).delete()
    classes.save()
    return HttpResponseRedirect(reverse("classes-detail", args=[class_id]))


def addStudentClass(request, class_id, student_id):
    classes = Class.objects.get(id=class_id)
    student = Student.objects.get(student_id=student_id)
    classes.student.add(student)
    classes.save()
    Attendance.objects.create(student=student, course=classes.course, classes=classes, absent_hours=0, attendance_rate=1.0)
    return HttpResponseRedirect(reverse("classes-detail", args=[class_id]))


def studentAttendance(request, student_id):
    student = Student.objects.get(student_id=student_id)
    classes_all = Class.objects.filter(student=student)
    attendance_all = Attendance.objects.filter(student=student)
    context = {"classes_all": classes_all, "attendance_all": attendance_all}
    return render(request, "studentattendance.html", context)


def checkMyAttendance(request, id):
    student = Student.objects.get(user=id)
    classes_all = Class.objects.filter(student=student)
    attendance_all = Attendance.objects.filter(student=student)
    context = {"classes_all": classes_all, "attendance_all": attendance_all}
    return render(request, "studentattendance.html", context)


def sendEmail(request):
    users = User.objects.all()
    if request.method == "POST":
        subject = request.POST.get("subject")
        body = request.POST.get("body")
        class_id = request.POST.get("class_id")
        receiver = User.objects.get(id=request.POST.get("user"))
        senderEmail = "mammuthus123@gmail.com"
        try:
            send_mail(subject, body, senderEmail, [receiver.email], fail_silently=False)
            return render(request, "emailsending.html", {
                "message": "email has been sent out",
                "users": users,
                "class_id": class_id
            })
        except:
            return render(request, "emailsending.html", {
                "message": "email sending failed",
                "users": users,
                "class_id": class_id
            })
    return render(request, "emailsending.html", {
        "message": "",
        "users": users
    })
