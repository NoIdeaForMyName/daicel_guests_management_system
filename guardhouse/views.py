import datetime
from datetime import tzinfo

from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.template import loader
from database_models.models import *
from guardhouse.forms import *
from guardhouse.services import ActiveGuestsService, GuestsHistoryService, \
    NotConfirmedArrivalsService
from database_models.models import Company, Guest, Car, Arrival, Responsibility
import hosts_API.functionalities as hosts_API
import json
from .security import validate_ip
from django.utils import timezone



@validate_ip
def home(request):
    template = loader.get_template('guardhouse/home.html')
    today_date = datetime.datetime.combine(datetime.datetime.today().date(), datetime.datetime.min.time())
    today_date = timezone.make_aware(today_date)
    print('aware:', today_date)
    old_active_guests = (Arrival.objects
                         .filter(confirmed=True)
                         .filter(leave_timestamp=None)
                         .filter(arrival_timestamp__lt=today_date)
                         .all())
    return HttpResponse(template.render({
        'old_guest_nb': len(old_active_guests)
    }))


@validate_ip
def active_guests(request):
    active_guests_service = ActiveGuestsService()

    if request.method == "POST":
        print("POST: ", request.POST)
        arrival_ids = request.POST.getlist('check[]')
        try:
            arrival_ids = [int(i) for i in arrival_ids]
        except:
            return HttpResponseBadRequest("Wrong request body - id should be a number")
        active_guests_service.end_arrivals(arrival_ids)
        return redirect("guardhouse-active-guests")

    template = loader.get_template('guardhouse/active_guests.html')

    active_guests_nb = active_guests_service.active_guests_count()
    guests_car_nb_at_workplace = active_guests_service.all_cars_at_workplace()

    active_arrivals, success = active_guests_service.active_arrivals_context()
    if not success:
        return active_arrivals, success # TODO
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
        return archive_arrivals, success # TODO
    archive_arrivals = archive_arrivals['message']

    return HttpResponse(template.render({
            'archive_arrivals': archive_arrivals
        }, request))


@validate_ip
def not_confirmed_visits(request):
    not_confirmed_arrivals_service = NotConfirmedArrivalsService()
    if request.method == "POST":
        arrival_ids = request.POST.getlist('check[]')
        try:
            arrival_ids = [int(i) for i in arrival_ids]
        except:
            return HttpResponseBadRequest("Wrong request body - id should be a number")
        register_nb = request.POST.get('register_nb')
        register_nb = register_nb if register_nb != '' else None
        message, success = not_confirmed_arrivals_service.confirm_arrivals(arrival_ids, register_nb)
        if not success:
            return message, success
        return redirect("guardhouse-not-confirmed-visits")
    template = loader.get_template('guardhouse/not_confirmed_visits.html')
    message, success = not_confirmed_arrivals_service.not_confirmed_arrivals_context()
    if not success:
        return message, success
    not_confirmed_arrivals = message['message']
    return HttpResponse(template.render({
        'not_confirmed_arrivals': not_confirmed_arrivals
    }, request))


# @validate_ip
# def confirm_visit(request, arrival_id):
#     template = loader.get_template('guardhouse/not_confirmed_visits.html')
#     confirm_service = ConfirmArrivalsService()
#     message, success = confirm_service.confirm_arrival(arrival_id)
#     if not success:
#         return message, success
#     return HttpResponse(template.render({
#
#     }, request))
