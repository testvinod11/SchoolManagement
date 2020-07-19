from django.urls import path

from . import views

urlpatterns = [
    path('', views.DashboardDetailView.as_view(), name=''),

    path('teacher', views.TeacherListView.as_view(), name='teacher-list'),
    path('teacher/create', views.TeacherCreateView.as_view(), name='teacher-create'),
    path('teacher/<int:pk>', views.TeacherDetailView.as_view(), name='teacher-detail'),
    path('teacher/<int:pk>/update', views.TeacherUpdateView.as_view(), name='teacher-update'),
    path('teacher/<int:pk>/delete', views.TeacherDeleteView.as_view(), name='teacher-delete'),

    path('student', views.StudentListView.as_view(), name='student-list'),
    path('student/create', views.StudentCreateView.as_view(), name='student-create'),
    path('student/<int:pk>', views.StudentDetailView.as_view(), name='student-detail'),
    path('student/<int:pk>/update', views.StudentUpdateView.as_view(), name='student-update'),
    path('student/<int:pk>/delete', views.StudentDeleteView.as_view(), name='student-delete'),
]
