from django.urls import reverse_lazy

from registration.common import *
from registration.models import Student, Teacher


class DashboardDetailView(ListView):
    model = Student
    template_name = 'registration/index.html'
    context_object_name = 'student'

    def get(self, request, *args, **kwargs):
        self.object_list = None
        teachers = Teacher.objects.filter(is_deleted=False).count()
        students = Student.objects.filter(is_deleted=False).count()
        return self.render_to_response({"teachers": teachers, "students": students})


class TeacherListView(CommonListView):

    model = Teacher
    view_for = "teacher"


class StudentListView(CommonListView):

    model = Student
    view_for = "student"


class TeacherDetailView(CommonDetailView):

    model = Teacher

    def get_context_data(self, **kwargs):
        """Insert the single object into the context dict."""
        students = self.object.students.filter(student__is_deleted=False).values('student_id', 'student__name', 'is_star_student')
        return super().get_context_data(queryset=students, view_for='teacher', **kwargs)


class StudentDetailView(CommonDetailView):

    model = Student

    def get_context_data(self, **kwargs):
        """Insert the single object into the context dict."""
        teachers = self.object.teachers.filter(teacher__is_deleted=False).values('teacher_id', 'teacher__name',
                                                                                 'is_star_student')
        return super().get_context_data(queryset=teachers, view_for='student', **kwargs)


class TeacherCreateView(CommonCreateView):
    model = Teacher
    success_url = reverse_lazy('teacher-list')
    view_for = 'teacher'


class StudentCreateView(CommonCreateView):
    model = Student
    success_url = reverse_lazy('student-list')
    view_for = 'student'


class StudentUpdateView(CommonUpdateView):

    model = Student
    view_for = 'student'

    def get_success_url(self):
        return reverse_lazy('student-detail', kwargs={'pk': self.object.id})


class TeacherUpdateView(CommonUpdateView):

    model = Teacher
    view_for = "teacher"

    def get_success_url(self):
        return reverse_lazy('teacher-detail', kwargs={'pk': self.object.id})


class TeacherDeleteView(CommonDeleteView):
    model = Teacher
    success_url = reverse_lazy('teacher-list')
    view_for = 'teacher'


class StudentDeleteView(CommonDeleteView):
    model = Student
    success_url = reverse_lazy('student-list')
    view_for = 'student'
