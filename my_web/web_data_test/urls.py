from django.urls import path
from . import views

urlpatterns = [
    path('', views.QueryStudent.as_view()),
]