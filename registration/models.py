from django.db import models


class RegistrationBaseModel(models.Model):
    name = models.CharField(max_length=100, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True


class Student(RegistrationBaseModel):

    def __str__(self):
        return f"{self.name}"


class Teacher(RegistrationBaseModel):

    def __str__(self):
        return f"{self.name}"


class TeacherStudentMap(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='students')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='teachers')
    is_star_student = models.BooleanField(default=False)

    class Meta:
        unique_together = ('teacher', 'student')

    def __str__(self):
        star_student = ", is star student." if self.is_star_student else ""
        return f"{self.teacher} have another student named is {self.student}{star_student}"
