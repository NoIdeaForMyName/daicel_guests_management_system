from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.template import loader
from database_models.models import *
from guardhouse.forms import *
from guardhouse.services import HostNewGuestsService, MeetingService, ActiveGuestsService, GuestsHistoryService
from database_models.models import Company, Guest, Car, Meeting, Arrival, Leadership, Responsibility
import hosts_API.functionalities as hosts_API
import json
from .security import validate_ip


@validate_ip
def home(request):
    template = loader.get_template('guardhouse/home.html')
    return HttpResponse(template.render())

@validate_ip
def add_guest(request):
    template = loader.get_template('guardhouse/add_guest.html')
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

@validate_ip
def add_guest_process(request):
    if request.method == "POST":
        data = json.loads(request.body)
        response, success = HostNewGuestsService.add_new_arrival_data(data)
        if success:
            return JsonResponse({"message": "Arrival added succesfully"}, status=200)
        else:
            return JsonResponse({"error": response}, status=400)
        #return JsonResponse({"message": "Guest added", "received": data})
    return JsonResponse({"error": "Incorrect method"}, status=400)


@validate_ip
def active_guests(request):
    active_guests_service = ActiveGuestsService()

    if request.method == "POST":
        print("POST: ", request.POST)
        arrival_ids = request.POST.getlist('end-visit[]')
        try:
            arrival_ids = [int(i) for i in arrival_ids]
        except:
            return HttpResponseBadRequest("Wrong request body - id should be a number")
        active_guests_service.end_arrivals(arrival_ids)
        return redirect("active-guests")

    template = loader.get_template('guardhouse/active_guests.html')

    active_guests_nb = active_guests_service.active_guests_count()
    guests_car_nb_at_workplace = active_guests_service.all_cars_at_workplace()

    active_arrivals, success = active_guests_service.active_arrivals_context()
    if not success:
        return active_arrivals # TODO
    active_arrivals = active_arrivals['message']

    return HttpResponse(template.render({
            'guest_nb': active_guests_nb,
            'cars_nb': guests_car_nb_at_workplace,
            'active_arrivals': active_arrivals
        }, request))


@validate_ip
def guests_history(request):
    guests_history_service = GuestsHistoryService()

    template = loader.get_template('guardhouse/guests_history.html')

    archive_arrivals, success = guests_history_service.archive_arrivals_context()
    if not success:
        return archive_arrivals # TODO
    archive_arrivals = archive_arrivals['message']

    return HttpResponse(template.render({
            'archive_arrivals': archive_arrivals
        }, request))
