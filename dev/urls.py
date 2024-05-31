from django.urls import path
from . import views

app_name = "dev"

urlpatterns = [
    path("upload", views.upload),
    path("upload-student-list", views.uploadStuList, name="upload-student-list"),
    path("upload-quiz", views.uploadQuiz, name="upload-quiz"),
    path("clear-all", views.clearAll, name="clear-all"),
]
