# chat/views.py
from django.http.response import HttpResponse
from django.shortcuts import render

def index(request):
    return HttpResponse("Index")

def room(request, room_name):
    return HttpResponse("room "+ room_name)