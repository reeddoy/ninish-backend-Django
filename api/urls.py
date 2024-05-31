from django.urls import path
from . import views

app_name = "api"

urlpatterns = [
    path("", views.index),
    path("quizzes/<int:pk>", views.getQuizzes),
    path("quizzesM/<int:pk>", views.getQuizzesMaster),
    path("login", views.login),
    path("modifyUser", views.modifyUser),
    path("conductingTime", views.getConductingTime),
    path("submit", views.submitForm),
    path("downloadCertificate/<int:regNum>", views.downloadCertificate),
    path("downloadCertificateV2/", views.downloadCertificateV2),
]
