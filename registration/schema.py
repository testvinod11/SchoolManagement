import graphene
from graphene_django import DjangoObjectType

from .models import *


class TeacherType(DjangoObjectType):
    class Meta:
        model = Teacher


class StudentType(DjangoObjectType):
    class Meta:
        model = Student


class Query(graphene.ObjectType):
    teachers = graphene.List(TeacherType)
    students = graphene.List(StudentType)

    def resolve_teachers(self, info, **kwargs):
        return Teacher.objects.filter(is_deleted=False)

    def resolve_students(self, info, **kwargs):
        return Student.objects.filter(is_deleted=False)


class AddTeacher(graphene.Mutation):
    id = graphene.Int()
    name = graphene.String()

    class Arguments:
        name = graphene.String()

    def mutate(self, info, name):
        teacher = Teacher(name=name, )
        teacher.save()

        return AddTeacher(
            id=teacher.id,
            name=teacher.name
        )


class AddStudent(graphene.Mutation):
    id = graphene.Int()
    name = graphene.String()

    class Arguments:
        name = graphene.String()

    def mutate(self, info, name):
        student = Student(name=name)
        student.save()

        return AddStudent(
            id=student.id,
            name=student.name
        )


class Mutation(graphene.ObjectType):
    add_teacher = AddTeacher.Field()
    add_student = AddStudent.Field()
