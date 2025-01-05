from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("indexxxx vejam bem !!!!")

def other(request):
    return HttpResponse("other pageeee by ianzera")
# Create your views here.
