from django.urls import path
from . import views

urlpatterns = [
    path('', views.QueryStudent.as_view()),
    path(r'get_main_data',views.get_main_data),
    path(r'update',views.load_data),
    path(r'get_label_liist',views.get_label_liist),
    path(r'delete_classroom',views.delete_classroom),
    path(r'login',views.login),
    path(r'edit_classroom',views.edit_classrooms),
    path(r'get_recycle_data', views.get_recycle_data),
]