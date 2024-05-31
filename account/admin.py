from django.contrib import admin
from .models import Student
from import_export import resources

class StudentsResources(resources.ModelResource):
    class Meta:
        model = Student
        fields = ('name','phone','registrationId','stu_class','institution','marks','quizTimeTaken','quizCategory')
        export_order = ('registrationId','name','stu_class','institution','phone','marks','quizTimeTaken','quizCategory')

# Register your models here.
admin.site.register(Student)