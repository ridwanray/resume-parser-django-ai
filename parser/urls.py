from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home_page"),
    path("upload-resume/", views.upload_resume, name="upload_resume"),
]
