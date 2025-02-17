from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from database_models.models import *
from django.forms import formset_factory
from guardhouse.forms import *


def home(request):
    template = loader.get_template('home.html')
    return HttpResponse(template.render())

def add_guest(request):
    template = loader.get_template('add_guest.html')
    PersonalDataFormSet = formset_factory(PersonalDataForm)
    if request.method == "POST":
        formset = PersonalDataFormSet(request.POST, request.FILES)
    else:
        formset = PersonalDataFormSet()
    return HttpResponse(template.render({"formset": formset}, request))
    return render(request, "add_guests.html", {"formset": formset})

def active_guests(request):
    template = loader.get_template('active_guests.html')
    return HttpResponse(template.render())

def guests_history(request):
    template = loader.get_template('guests_history.html')
    return HttpResponse(template.render())
