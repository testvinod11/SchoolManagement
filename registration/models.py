from django.db import models


class CustomManager(models.Manager):
    def get_queryset(self):
        return super(CustomManager, self).get_queryset().filter(is_deleted=False)


class BaseDateModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class RegistrationBaseModel(BaseDateModel):
    name = models.CharField(max_length=100, null=False)
    is_deleted = models.BooleanField(default=False)

    objects = CustomManager()

    class Meta:
        abstract = True


class Student(RegistrationBaseModel):

    def __str__(self):
        return f"{self.name}"


class Teacher(RegistrationBaseModel):

    def __str__(self):
        return f"{self.name}"


class TeacherStudentMap(BaseDateModel):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='students')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='teachers')
    is_star_student = models.BooleanField(default=False)
    is_associate = models.BooleanField(default=False)

    class Meta:
        unique_together = ('teacher', 'student')

    def __str__(self):
        star_student = ", is star student." if self.is_star_student else ""
        return f"{self.teacher} have another student named is {self.student}{star_student}"
