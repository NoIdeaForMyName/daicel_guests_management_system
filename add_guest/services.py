from database_models.models import *
import hosts_API.functionalities as hosts_API
from datetime import datetime, time
from daicel_guests_management_system.constants import *
from django.db import transaction
from django.utils import timezone


@transaction.atomic
def add_new_arrival_data(data):

    print("JSON:", data)

    confirmed = bool(data['confirmed'])

    company_name = data['company']
    register_nb = data['register_number']
    guests = data['guests']
    description = data['description']
    hosts = data['hosts']
    print('hosts:', hosts)

    company_m = None
    car_m = None
    guests_m = []
    arrivals_m = []
    hosts_m_API = []

    all_hosts, success = hosts_API.get_all_hosts_data()
    if not success:
        return all_hosts, success
    all_hosts = set(all_hosts['message'])

    if company_name:
        company_m = Company.objects.filter(name=company_name).first()
        if company_m is None:
            company_m = Company(name=company_name)
            company_m.save()

    if register_nb:
        if not Car.validate_register_number(register_nb):
            transaction.set_rollback(True)
            return {'error': f"Incorrect register number {register_nb}"}, False
        car_m = Car.objects.filter(register_number=register_nb).first()
        if car_m is None:
            car_m = Car(register_number=register_nb)
            car_m.save()

    for guest in guests:
        guest_m = None
        if guest['id'] != -1:
            guest_m = Guest.objects.filter(id=guest['id']).first()
            if guest_m == None or (guest_m.firstname, guest_m.lastname) != (guest['firstname'], guest['lastname']):
                transaction.set_rollback(True)
                return {'error': f"Provided guest id doesn't match the one from the database"}, False
        else:
            guest_m = Guest(
                firstname=guest['firstname'],
                lastname=guest['lastname'],
            )
        guest_m.save()
        guests_m.append(guest_m)

    for host_API in hosts:
        # host_m_API = [host for host in all_hosts if (host.id, host.firstname, host.lastname) == (host_API['id'], host_API['firstname'], host_API['lastname'])]
        # host_m_API = None if host_m_API == [] else host_m_API
        host_m_API = hosts_API.FullHost(**host_API)
        if not host_m_API in all_hosts:
            transaction.set_rollback(True)
            return {'error': f"Given host: {host_API} doesn't exists in the database"}, False
        hosts_m_API.append(host_m_API)

    for guest_m in guests_m:
        arrival_m = Arrival(
            confirmed=confirmed,
            guest=guest_m,
            arrival_purpose=description,
            car=car_m,
            arrival_timestamp=timezone.now() if confirmed else None,
            company=company_m
        )
        arrival_m.save()
        arrivals_m.append(arrival_m)

        for host_m_API in hosts_m_API:
            responsibility_m = Responsibility(
                host=host_m_API.id,
                arrival=arrival_m
            )
            responsibility_m.save()

        arrival_m.save()

    return {'message': f"Arrivals added succesfully: {data}"}, True
