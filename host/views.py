from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.template import loader
from database_models.models import *
from database_models.models import Company, Guest, Car, Arrival, Responsibility
import hosts_API.functionalities as hosts_API
import json
from .services import *

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from .forms import LoginForm

def login_host(request):
    template = loader.get_template('host/login.html')
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            next_ = form.cleaned_data['next']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(next_)
            else:
                return HttpResponse(template.render({
                    "wrong_credentials": True,
                    "form": LoginForm(initial={'next': next_})
                }, request))
    else:
        return HttpResponse(template.render({
            "wrong_credentials": False,
            "form": LoginForm(initial={'next': request.GET['next']})
        }, request))

@login_required(login_url="/host/login/")
def home(request):
    template = loader.get_template('host/home.html')
    return HttpResponse(template.render())


@login_required(login_url="/host/login/")
def my_guests(request):
    template = loader.get_template('host/my_guests.html')
    return HttpResponse(template.render())

def not_confirmed_guests(request):
    service = HostNotConfirmedGuestsService(request.user.id)
    guests_data, success = service.get_not_confirmed_guests()
    if not success:
        return guests_data, success
    guests_data = guests_data['message']
    return render(request, 'host/not_confirmed_guests.html', {
        'not_confirmed_guests': guests_data
    })

@login_required(login_url="/host/login/")
def active_guests(request):
    service = HostActiveGuestsService(request.user.id)
    guests_data, success = service.get_active_guests()
    if not success:
        return guests_data, success
    guests_data = guests_data['message']
    return render(request, 'host/active_guests.html', {
        'active_guests': guests_data
    })

@login_required(login_url="/host/login/")
def guests_history(request):
    service = HostGuestsHistoryService(request.user.id)
    history_data, success = service.get_guests_history()
    if not success:
        return history_data, success
    history_data = history_data['message']
    return render(request, 'host/guests_history.html', {
        'guests_history': history_data
    })
