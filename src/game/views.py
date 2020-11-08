# chat/views.py
from django.http.response import HttpResponse
from django.shortcuts import render

def index(request):
    return HttpResponse("Index")

def game(request, game_slug):
    return HttpResponse("game "+ game_slug)