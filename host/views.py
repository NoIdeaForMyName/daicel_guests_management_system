from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.template import loader
from database_models.models import *
from database_models.models import Company, Guest, Car, Meeting, Arrival, Leadership, Responsibility
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
def add_meeting(request):
    template = loader.get_template('host/add_meeting.html')
    hosts, success = hosts_API.get_all_hosts_data_dict()
    if not success: # TODO
        return hosts, success
    hosts = hosts['message']
    author = None
    for leader in hosts:
        if request.user.id == leader['id']:
            author = leader
            break
    if author is None: # TODO
        return HttpResponseBadRequest()
    return HttpResponse(template.render({
        "hosts": hosts,
        "author": author
    }, request))

@login_required(login_url="/host/login/")
def add_meeting_process(request):
    print('LOLZ AM HERE')
    if request.method == "POST":
        data = json.loads(request.body)
        response, success = add_new_meeting(data)
        if success:
            return JsonResponse({"message": "Arrival added succesfully"}, status=200)
        else:
            return JsonResponse(response, status=400)
    return JsonResponse({"error": "Incorrect method"}, status=400)

@login_required(login_url="/host/login/")
def my_guests(request):
    template = loader.get_template('host/my_guests.html')
    return HttpResponse(template.render())

@login_required(login_url="/host/login/")
def my_meetings(request):
    template = loader.get_template('host/my_meetings.html')
    return HttpResponse(template.render())

@login_required(login_url="/host/login/")
def led_meetings(request):
    template = loader.get_template('host/led_meetings.html')
    return HttpResponse(template.render())
