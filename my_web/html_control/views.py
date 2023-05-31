from django.shortcuts import render
from django.http import HttpResponse
def index(request):
    return HttpResponse(r"I am html")
def test(request):
    return HttpResponse(r"I am the test")

def html(request):
    return render(request,"check.html")
def main_index(request):
    return render(request,"main.html")

def map_index(request):
    return render(request,"map.html")

def select_classroom_index(request):
    return render(request, "select_classroom.html")

def login_index(request):
    return render(request, "login.html")

def edit_classroom_index(request):
    return render(request, "edit_classroom.html")

def recycle_index(request):
    return render(request, "recycle.html")
