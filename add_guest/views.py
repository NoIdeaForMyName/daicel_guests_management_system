from django.shortcuts import render, loader
from django.http import HttpResponse, JsonResponse
from database_models.models import *
from hosts_API.functionalities import *
from .services import *

def add_guest(request, src):
    template = loader.get_template('add_guest/add_guest.html')
    hosts, success = hosts_API.get_all_hosts_data_dict()
    if not success:
        return hosts # TODO
    hosts = hosts['message']
    companies = list(Company.objects.all().values())
    guests = list(Guest.objects.all().values())
    author = None
    if src == "host": # host site
        base_template = 'host/master.html'
        process_url = '/host/add-guest-process'
        redirect_url = '/host/not-confirmed-guests'
        confirmed = False
        for host in hosts:
            if host['id'] == request.user.id:
                author = host
                break
    else:
        base_template = 'guardhouse/master.html'
        process_url = '/guardhouse/add-guest-process'
        redirect_url = '/guardhouse/active-guests'
        confirmed = True
    return HttpResponse(template.render({
        "base_template": base_template,
        "process_url": process_url,
        "redirect_url": redirect_url,
        "author": author,
        "confirmed": confirmed,
        "companies_data": companies,
        "registered_guests_data": guests,
        "hosts_data": hosts
        }, request))


def add_guest_process(request):
    if request.method == "POST":
        data = json.loads(request.body)
        response, success = add_new_arrival_data(data)
        if success:
            return JsonResponse({"message": "Wizyta dodana pomyślnie"}, status=200)
        else:
            return JsonResponse(response, status=400)
        #return JsonResponse({"message": "Guest added", "received": data})
    return JsonResponse({"error": "Niepoprawne żądanie"}, status=400)
