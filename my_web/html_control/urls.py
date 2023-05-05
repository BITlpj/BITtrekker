from django.urls import path
from . import views

urlpatterns = [
    path(r'index',views.index),
    path(r'test',views.test),
    path(r'check',views.html),
]