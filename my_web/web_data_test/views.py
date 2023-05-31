import json

from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse
from django.http import JsonResponse
from .models import Classroom,LabelClassroom,Labeltable,Occupytable # 引用上一把创建的数据表
from .utils import *
import os
from .test import pachong
class QueryStudent(APIView):
    @staticmethod
    def get(request):
        return Response(True)
    '''
    def get(request):
        """
        """
        req = request.query_params.dict()#前端给的json包数据
        student_name = req["student_name"]

        student_id = Student.objects.filter(student_name=student_name).values("student_id")#提取数据表中数据
        return Response(student_id)#返回数据，这里由于提取数据表中数据直接就是jason格式所以可以直接传，其他的需要转为json格式
    @staticmethod
    def post(request):
        """
        """
        req = request.data#前端给的json包数据
        student_id = req["student_id"]
        student_name = req["student_name"]

        Student(student_id=student_id,student_name=student_name).save()#保存数据

        return Response()#不需要返回数据
'''

def get_main_data(request):
    req = request.body.decode("utf-8")
    ans = json.loads(req)
    class_info= ask_class_info(ans)
    return JsonResponse(class_info,safe=False)
def load_data(request):
    clear_all_database()
    req = request.body.decode("GBK")
    json_data=json.loads(req)
    if json_data['pachong']==True:
        pachong()
    for i in os.listdir("D:\python web\my_web\web_data_test"):
        if i.split('.')[-1]=="json":
            update_data(os.path.join("D:\python web\my_web\web_data_test",i))
    return HttpResponse(True)

def get_label_liist(request):
    ans=ask_label_table()
    return JsonResponse(ans)

def delete_classroom(request):
    req = request.body.decode("utf-8")
    ans = json.loads(req)
    cover_classroom(ans["classroom_number",1])

def login(request):

    return HttpResponse(True)

def edit_classrooms(request):
    req = request.body.decode("utf-8")
    ans = json.loads(req)
    ans=edit_classroom(ans)
    return  HttpResponse(ans)

def get_recycle_data(request):
    req = request.body.decode("utf-8")
    ans = json.loads(req)
    ans = ask_class_info(ans)
    return JsonResponse(ans)