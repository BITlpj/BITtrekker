from django.shortcuts import render
from django.http import HttpResponse
def index(request):
    return HttpResponse(r"I am html")
def test(request):
    return HttpResponse(r"I am the test")

def html(request):
    return render(request,"check.html")