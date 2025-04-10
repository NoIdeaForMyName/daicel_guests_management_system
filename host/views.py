from django.contrib.messages import success
from django.forms import model_to_dict
from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.template import loader
from django.urls import reverse

from database_models.models import *
from database_models.models import Company, Guest, Car, Arrival, Responsibility
import hosts_API.functionalities as hosts_API
import json
from .services import *

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
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
def logout_host(request):
    logout(request)
    return redirect('main-menu-home')

@login_required(login_url="/host/login/")
def home(request):
    template = loader.get_template('host/home.html')
    not_confirmed_guests_nb = len(HostNotConfirmedGuestsService(request.user.id).not_confirmed_guests)
    active_guests_nb = len(HostActiveGuestsService(request.user.id).active_arrivals)
    return HttpResponse(template.render({
        'not_confirmed_arrivals_nb': not_confirmed_guests_nb,
        'active_arrivals_nb': active_guests_nb
    }))


@login_required(login_url="/host/login/")
def my_guests(request):
    template = loader.get_template('host/my_guests.html')
    return HttpResponse(template.render())

@login_required(login_url="/host/login/")
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


@login_required
def edit_guest(request, arrival_id):
    not_confirmed_guests_service = HostNotConfirmedGuestsService(request.user.id)

    if request.method == "POST":
        data = json.loads(request.body)
        response, success = not_confirmed_guests_service.update_arrival(data)
        if success:
            return JsonResponse({'message': 'Wizyta edytowana pomyślnie'})
        else:
            return JsonResponse({"error": response}, status=400)
        # return JsonResponse({"message": "Guest added", "received": data})

    arrival = get_object_or_404(Arrival, id=arrival_id)

    # Sprawdź uprawnienia
    if not Responsibility.objects.filter(host=request.user.id, arrival=arrival).exists():
        return HttpResponseForbidden("Brak uprawnień do edycji tego gościa")

    # Przygotuj dane kontekstowe
    hosts_data, success = hosts_API.get_all_hosts_data_dict()
    if not success:
        return hosts_data, success
    hosts_data = hosts_data['message']
    company = arrival.company.name if arrival.company else ''
    host_ids = set(r.host for r in arrival.responsibility_set.all())
    hosts = [host for host in hosts_data if host['id'] in host_ids]

    context = {
        'companies_data': list(Company.objects.all().values()),
        'hosts_data': hosts_data,
        'registered_guests_data': list(Guest.objects.all().values()),
        #'process_url': reverse('host-edit-guest', arrival_id),
        'process_url': f'/host/edit_guest/{arrival_id}/',
        'redirect_url': '/host/not-confirmed-guests',
        'confirmed': arrival.confirmed,
        'author': [h for h in hosts_data if h['id'] == request.user.id][0],
        'arrival_data': {
            'id': arrival.id,
            'company': company,
            'register_number': arrival.car.register_number if arrival.car else '',
            'description': arrival.arrival_purpose,
            'guest': model_to_dict(arrival.guest),
            'hosts': hosts
        }
    }
    return render(request, 'host/edit_guest.html', context)

@login_required
def delete_guest(request, arrival_id):
    if request.method != "POST":
        return JsonResponse({"error": "Niepoprawna metoda HTTP"}, status=400)
    not_confirmed_guests_service = HostNotConfirmedGuestsService(request.user.id)
    message, success = not_confirmed_guests_service.delete_arrival(arrival_id)
    if not success:
        return JsonResponse(message, status=400)
    return redirect('host-not-confirmed-guests')


