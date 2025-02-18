from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from database_models.models import *
from guardhouse.forms import *
from guardhouse.db_functionalities import *


def home(request):
    template = loader.get_template('home.html')
    return HttpResponse(template.render())

def add_guest(request):
    template = loader.get_template('add_guest.html')
    hosts, success = get_all_hosts()
    if not success:
        return hosts # TODO
    meetings, success = get_active_meetings_full_data()
    if not success:
        return meetings # TODO
    companies = ["Electrolux, Whirlpool"] # TODO
    return HttpResponse(template.render({
        "companies_data": companies,
        "registered_users_data": hosts['message'], # TODO
        "hosts_data": hosts['message'],
        "meetings_data": meetings['message']
        }, request))
    #return render(request, "add_guests.html", {"formset": formset})

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
