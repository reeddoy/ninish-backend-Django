from django.shortcuts import HttpResponse
from .models import Student
from .admin import StudentsResources

def index(request):
    students = Student.objects.filter()
    dataset = StudentsResources().export(students)
    dataset = dataset.xls

    response = HttpResponse(dataset, content_type="xls")
    response["Content-Disposition"] = f"attachment; filename=student_list.xls"
    return response