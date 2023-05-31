from django.urls import path
from . import views

urlpatterns = [
    path(r'index',views.index),
    path(r'test',views.test),
    path(r'check',views.html),
    path(r'map',views.map_index),
    path(r'main',views.main_index),
    path(r'select_classroom',views.select_classroom_index),
    path(r'login',views.login_index),
    path(r'edit_classroom',views.edit_classroom_index),
    path(r'recycle',views.recycle_index),
]