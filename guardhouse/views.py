from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader
from database_models.models import *
from guardhouse.forms import *
from guardhouse.db_functionalities import *
import json


def home(request):
    template = loader.get_template('home.html')
    return HttpResponse(template.render())

def add_guest(request):
    template = loader.get_template('add_guest.html')
    hosts, success = get_all_hosts()
    if not success:
        return hosts # TODO
    meetings, success = get_active_meetings_full_data()
    #print("test meeting:", meetings)
    if not success:
        return meetings # TODO
    companies = get_all_companies()
    guests = get_all_known_guests()
    return HttpResponse(template.render({
        "companies_data": companies,
        "registered_guests_data": guests,
        "hosts_data": hosts['message'],
        "meetings_data": meetings['message']
        }, request))
    #return render(request, "add_guests.html", {"formset": formset})

# from django.views.decorators.csrf import csrf_exempt
# @csrf_exempt
def add_guest_process(request):
    if request.method == "POST":
        data = json.loads(request.body)
        response, success = add_new_arrival_data(data)
        return JsonResponse(response, status=(400 if not success else 200))
        #return JsonResponse({"message": "Guest added", "received": data})
    return JsonResponse({"error": "Incorrect method"}, status=400)

# def add_guest(request):
#     template = loader.get_template('add_guest.html')
#     #PersonalDataFormSet = formset_factory(PersonalDataForm)
#     if request.method == "POST":
#         collective_guests_data_form = CollectiveGuestsDataForm(request.POST)
#         guest_formset = GuestFormset(request.POST)
#         if collective_guests_data_form.is_valid():
#             print(collective_guests_data_form.cleaned_data)
#         if guest_formset.is_valid():
#             for x in guest_formset.cleaned_data:
#                 print(x)
#     else:
#         collective_guests_data_form = CollectiveGuestsDataForm()
#         guest_formset = GuestFormset()
#     return HttpResponse(template.render({
#         "collective_guest_data_form": collective_guests_data_form,
#         "guest_formset": guest_formset,
#         "hosts_data": get_all_hosts()
#         }, request))
#     #return render(request, "add_guests.html", {"formset": formset})

def active_guests(request):
    template = loader.get_template('active_guests.html')
    return HttpResponse(template.render())

def guests_history(request):
    template = loader.get_template('guests_history.html')
    return HttpResponse(template.render())
