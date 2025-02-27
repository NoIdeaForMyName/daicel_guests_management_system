from django.shortcuts import render, loader
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest


def home(request):
    template = loader.get_template('main_menu/home.html')
    return HttpResponse(template.render())
