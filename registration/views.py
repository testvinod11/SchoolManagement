# Django imports
from django.db import IntegrityError
from django.http import JsonResponse, HttpResponseNotFound
from django.urls import reverse_lazy

# Local imports
from registration.common import *
from registration.models import Student, Teacher, TeacherStudentMap


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
        student_qs = self.object.students.filter(student__is_deleted=False, is_associate=True).order_by('-updated_at')
        associate_student_qs = student_qs.values('student_id', 'student__name', 'is_star_student')
        non_associate_student_qs = Student.objects.exclude(
            id__in=student_qs.values_list('student_id', flat=True)).values('id', 'name')
        return super().get_context_data(
            queryset=associate_student_qs, non_associate_qs=non_associate_student_qs, view_for='teacher', **kwargs)


class StudentDetailView(CommonDetailView):

    model = Student

    def get_context_data(self, **kwargs):
        """Insert the single object into the context dict."""
        teacher_qs = self.object.teachers.filter(teacher__is_deleted=False, is_associate=True).order_by('-updated_at')
        associate_teacher_qs = teacher_qs.values('teacher_id', 'teacher__name', 'is_star_student')
        non_associate_teacher_qs = Teacher.objects.exclude(
            id__in=teacher_qs.values_list("teacher_id", flat=True)).values('id', 'name')
        return super().get_context_data(
            queryset=associate_teacher_qs, non_associate_qs=non_associate_teacher_qs, view_for='student', **kwargs)


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


def process_(request, param):
    """
    Function is used for precess request and fetch TeacherStudentMap instance
    :param request: request
    :param param: param
    :return: tuple of status, param, and object(it can be either TeacherStudentMap or HttpResponseNotFound)
    """
    student_id = request.GET.get('studentId', None)
    teacher_id = request.GET.get('teacherId', None)
    param = request.GET.get(param, None)
    if not student_id or not teacher_id or not param:
        return False, param, HttpResponseNotFound()
    try:
        obj, _ = TeacherStudentMap.objects.get_or_create(teacher_id=teacher_id, student_id=student_id)
    except IntegrityError:
        return False, param, HttpResponseNotFound()
    return True, param, obj


def associate_teacher_student(request):
    """

    :param request:
    :return:
    """
    status, associate, obj = process_(request, "associate")
    if status:
        if associate == 'true':
            obj.is_associate = True
            data = {'message': "Successfully associate", 'id': obj.student_id, 'teacher_id': obj.teacher_id, 'is_star_student':obj.is_star_student}
        else:
            obj.is_associate = False
            obj.is_star_student = False
            data = {'message': "Successfully un-associate", 'id': obj.student_id, 'teacher_id':obj.teacher_id, 'is_star_student':obj.is_star_student}
        obj.save()
        return JsonResponse(data)
    return obj


def star_student(request):
    """

    :param request:
    :return:
    """
    status, is_star_student, obj = process_(request, "starStudent")
    if status:
        if is_star_student == "true":
            obj.is_star_student = True
            data = {'message': "Successfully student make a star student"}
        else:
            obj.is_star_student = False
            data = {'message': "Successfully un-associate"}
        obj.save()
        return JsonResponse(data)
    return obj
