from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.template import loader
from database_models.models import *
from database_models.models import Company, Guest, Car, Meeting, Arrival, Leadership, Responsibility
import hosts_API.functionalities as hosts_API
import json


def home(request):
    template = loader.get_template('host/home.html')
    return HttpResponse(template.render())

def new_meeting(request):
    template = loader.get_template('host/new_meeting.html')
    return HttpResponse(template.render())

def my_guests(request):
    template = loader.get_template('host/my_guests.html')
    return HttpResponse(template.render())

def my_meetings(request):
    template = loader.get_template('host/my_meetings.html')
    return HttpResponse(template.render())

def led_meetings(request):
    template = loader.get_template('host/led_meetings.html')
    return HttpResponse(template.render())
