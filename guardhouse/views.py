from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader
from database_models.models import *
from guardhouse.forms import *
from guardhouse.services import HostNewGuestsService, MeetingService
from database_models.models import Company, Guest, Car, Meeting, Arrival, Participation, Leadership, Responsibility
import hosts_API.functionalities as hosts_API
import json


def home(request):
    template = loader.get_template('home.html')
    return HttpResponse(template.render())

def add_guest(request):
    template = loader.get_template('add_guest.html')
    hosts, success = hosts_API.get_all_hosts_data_dict()
    if not success:
        return hosts # TODO
    meetings, success = MeetingService.get_active_meetings_full_data()
    #print("test meeting:", meetings)
    if not success:
        return meetings # TODO
    companies = list(Company.objects.all().values())
    guests = list(Guest.objects.all().values())
    return HttpResponse(template.render({
        "companies_data": companies,
        "registered_guests_data": guests,
        "hosts_data": hosts['message'],
        "meetings_data": meetings['message']
        }, request))

def add_guest_process(request):
    if request.method == "POST":
        data = json.loads(request.body)
        response, success = HostNewGuestsService.add_new_arrival_data(data)
        return JsonResponse(response, status=(400 if not success else 200))
        #return JsonResponse({"message": "Guest added", "received": data})
    return JsonResponse({"error": "Incorrect method"}, status=400)


def active_guests(request):
    template = loader.get_template('active_guests.html')
    return HttpResponse(template.render())


def guests_history(request):
    template = loader.get_template('guests_history.html')
    return HttpResponse(template.render())
