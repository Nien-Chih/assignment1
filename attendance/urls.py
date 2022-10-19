from django.urls import path, include

from attendance.views import semester, semesterDetail, createSemester, updateSemester, deleteSemester, course, \
    courseDetail, createCourse, updateCourse, deleteCourse, classes, classesDetail, createClasses, updateClasses, \
    deleteClasses, lecturer, lecturerDetail, createLecturer, updateLecturer, deleteLecturer, student, studentDetail, \
    createStudent, updateStudent, deleteStudent, file_upload, RegistrationView, CustomRegistration, index, \
    studentClassesDetail, studentClasses, deleteStudentClass, getSemesterByCourseId, addStudentClass, studentAttendance, \
    lecturerAttendance, lecturerAttendanceDetail, saveAttendance, sendEmail, checkMyAttendance, attendanceCourses

urlpatterns = [
    path("", index, name='index'),
    path("semester/course_id/<int:course_id>", getSemesterByCourseId, name='get-semester-by-course_id'),
    path("semester", semester, name='get-semester'),
    path("semester/<int:semester_id>/detail", semesterDetail, name='semester-detail'),
    path("semester/create", createSemester, name="create-semester"),
    path("semester/update", updateSemester, name="update-semester"),
    path("semester/<int:semester_id>/delete", deleteSemester, name='delete-semester'),

    path("course", course, name='get-course'),
    path("course/<int:course_id>/detail", courseDetail, name='course-detail'),
    path("course/create", createCourse, name="create-course"),
    path("course/update", updateCourse, name="update-course"),
    path("course/<int:course_id>/delete", deleteCourse, name='delete-course'),

    path("classes", classes, name='get-classes'),
    path("classes/<int:classes_id>/detail", classesDetail, name='classes-detail'),
    path("classes/create", createClasses, name="create-classes"),
    path("classes/update", updateClasses, name="update-classes"),
    path("classes/<int:classes_id>/delete", deleteClasses, name='delete-classes'),

    path("lecturer", lecturer, name='get-lecturer'),
    path("lecturer/<int:staff_id>/detail", lecturerDetail, name='lecturer-detail'),
    path("lecturer/create", createLecturer, name="create-lecturer"),
    path("lecturer/update", updateLecturer, name="update-lecturer"),
    path("lecturer/<int:staff_id>/delete", deleteLecturer, name='delete-lecturer'),
    path("lecturer/<int:staff_id>/attendance", lecturerAttendance, name='lecturer-attendance'),
    path("lecturer/<int:class_id>/attendance/detail", lecturerAttendanceDetail, name='attendance-detail'),
    path("attendance_course", attendanceCourses, name='get-attendance-course'),
    path("save_attendance", saveAttendance, name='save-attendance'),

    path("student", student, name='get-student'),
    path("student/<int:student_id>/detail", studentDetail, name='student-detail'),
    path("student/create", createStudent, name="create-student"),
    path("student/update", updateStudent, name="update-student"),
    path("student/<int:student_id>/delete", deleteStudent, name='delete-student'),
    path("student/classes", studentClasses, name='get-student-classes'),
    path("student/classes/<int:class_id>/detail", studentClassesDetail, name='student-classes-detail'),
    path("student/classes/<int:class_id>/student/<int:student_id>/delete", deleteStudentClass,
         name='delete-student-class'),
    path("student/classes/<int:class_id>/student/<int:student_id>/add", addStudentClass, name='add-student-class'),
    path("student/<int:student_id>/attendance", studentAttendance, name='get-student-attendance'),
    path("check/<int:id>/myattendance", checkMyAttendance, name='check-my-attendance'),

    path('file_upload', file_upload, name='file-upload'),

    path("accounts/create", RegistrationView.as_view(), name="register"),
    path("accounts/custom_create", CustomRegistration, name="custom_register"),
    path("accounts/", include("django.contrib.auth.urls")),
    # path("accounts/login", login, name="login"),
    path("send_email", sendEmail, name="send_email")
]
