from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import Http404
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

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


class StudentListView(ListView):

    model = Student
    template_name = 'registration/student/list.html'
    context_object_name = 'students'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(StudentListView, self).get_context_data(**kwargs)
        students = self.get_queryset()
        page = self.request.GET.get('page')
        paginator = Paginator(students, self.paginate_by)
        try:
            students = paginator.page(page)
        except PageNotAnInteger:
            students = paginator.page(1)
        except EmptyPage:
            students = paginator.page(paginator.num_pages)
        context['students'] = students
        return context

    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False).order_by('-id')


class StudentCreateView(CreateView):
    model = Student
    template_name = 'registration/student/create.html'
    fields = ('name', )
    success_url = reverse_lazy('student-list')


class StudentDetailView(DetailView):

    model = Student
    template_name = 'registration/student/detail.html'
    context_object_name = 'student'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.is_deleted:
            raise Http404("No object found matching the query")
        teachers = self.object.teachers.filter(teacher__is_deleted=False)
        context = self.get_context_data(object=self.object, teachers=teachers)
        return self.render_to_response(context)


class StudentUpdateView(UpdateView):

    model = Student
    template_name = 'registration/student/update.html'
    context_object_name = 'student'
    fields = ('name',)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.is_deleted:
            raise Http404("No object found matching the query")
        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('student-detail', kwargs={'pk': self.object.id})


class StudentDeleteView(DeleteView):
    model = Student
    template_name = 'registration/student/delete.html'
    success_url = reverse_lazy('student-list')

    def delete(self, request, *args, **kwargs):
        """
        Call the delete() method on the fetched object and then redirect to the
        success URL.
        """
        self.object = self.get_object()
        if self.object.is_deleted:
            raise Http404("No object found matching the query")
        success_url = self.get_success_url()
        self.object.is_deleted = True
        self.object.save()
        return HttpResponseRedirect(success_url)


class TeacherListView(ListView):

    model = Teacher
    template_name = 'registration/teacher/list.html'
    context_object_name = 'teachers'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(TeacherListView, self).get_context_data(**kwargs)
        teachers = self.get_queryset()
        page = self.request.GET.get('page')
        paginator = Paginator(teachers, self.paginate_by)
        try:
            teachers = paginator.page(page)
        except PageNotAnInteger:
            teachers = paginator.page(1)
        except EmptyPage:
            teachers = paginator.page(paginator.num_pages)
        context['teachers'] = teachers
        return context

    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False).order_by('-id')


class TeacherCreateView(CreateView):
    model = Teacher
    template_name = 'registration/teacher/create.html'
    fields = ('name', )
    success_url = reverse_lazy('teacher-list')


class TeacherDetailView(DetailView):

    model = Teacher
    template_name = 'registration/teacher/detail.html'
    context_object_name = 'teacher'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.is_deleted:
            raise Http404("No object found matching the query")
        students = self.object.students.filter(student__is_deleted=False)
        context = self.get_context_data(object=self.object, students=students)
        return self.render_to_response(context)


class TeacherUpdateView(UpdateView):

    model = Teacher
    template_name = 'registration/teacher/update.html'
    context_object_name = 'teacher'
    fields = ('name',)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.is_deleted:
            raise Http404("No object found matching the query")
        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('teacher-detail', kwargs={'pk': self.object.id})


class TeacherDeleteView(DeleteView):
    model = Teacher
    template_name = 'registration/teacher/delete.html'
    success_url = reverse_lazy('teacher-list')

    def delete(self, request, *args, **kwargs):
        """
        Call the delete() method on the fetched object and then redirect to the
        success URL.
        """
        self.object = self.get_object()
        if self.object.is_deleted:
            raise Http404("No object found matching the query")
        success_url = self.get_success_url()
        self.object.is_deleted = True
        self.object.save()
        return HttpResponseRedirect(success_url)
