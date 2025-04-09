from datetime import datetime
from django.db import transaction

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from daicel_guests_management_system.constants import DATETIME_FORMAT
from database_models.models import *
import hosts_API.functionalities as hosts_API


class HostNotConfirmedGuestsService:
    def __init__(self, user_id):
        self.user_id = user_id
        self.not_confirmed_guests = (Responsibility.objects
                                     .filter(host=user_id)
                                     .select_related('arrival')
                                     .filter(arrival__confirmed=False)
                                     .select_related('arrival__guest')
                                     .select_related('arrival__car')
                                     .select_related('arrival__company')
                                     .prefetch_related('arrival__responsibility_set')
                                     .distinct()
                                     )

    def get_not_confirmed_guests(self):
        full_hosts, success = hosts_API.get_all_hosts_data()
        if not success:
            return full_hosts, success
        full_hosts = full_hosts['message']

        seen = set()
        result = []
        for resp in self.not_confirmed_guests:
            arrival = resp.arrival
            if arrival.id in seen:
                continue
            seen.add(arrival.id)

            host_ids = [r.host for r in arrival.responsibility_set.all()]
            hosts = []
            for host_id in host_ids:
                host = next((h for h in full_hosts if h.id == host_id), None)
                if host:
                    hosts.append({'name': f"{host.firstname} {host.lastname}"})

            result.append({
                'id': arrival.id,
                'name': f"{arrival.guest.firstname} {arrival.guest.lastname}",
                'company': arrival.company.name if arrival.company else None,
                'description': arrival.arrival_purpose,
                'hosts': hosts
            })

        return {'message': result}, True

    @transaction.atomic
    def update_arrival(self, data):
        # {'arrival_id': '50', 'confirmed': False, 'company': 'Electrolux', 'register_number': '', 'description': 'spotkanie testowe', 'hosts': [{'id': 3, 'firstname': 'Tadeusz', 'lastname': 'Nowak'}, {'id': 4, 'firstname': 'Mariusz', 'lastname': 'Wiśniewski'}]}
        try:
            arrival_m = self.not_confirmed_guests.get(arrival__id=data['arrival_id']).arrival
            #arrival_m = Arrival.objects.filter(confirmed=False).get(data['arrival_id'])
        except ObjectDoesNotExist:
            transaction.set_rollback(True)
            return {'error': f'Wizyta o id: {data['arrival_id']} nie istnieje lub nie masz uprawnień do jej edycji'}, False
        try:
            company = Company.objects.get(name=data['company'])
        except ObjectDoesNotExist:
            company = Company(name=data['company'])
            company.save()
        arrival_m.company = company
        try:
            car = Car.objects.get(register_number=data['register_number'])
        except ObjectDoesNotExist:
            car = Car(register_number=data['register_number'])
            car.save()
        arrival_m.car = car
        arrival_m.arrival_purpose = data['description']
        arrival_m.arrival_timestamp = None
        arrival_m.leave_timestamp = None
        arrival_hosts_ids = [host['id'] for host in data['hosts']]
        all_hosts, success = hosts_API.get_all_hosts_data()
        if not success:
            return all_hosts, success
        all_hosts = all_hosts['message']
        known_hosts_ids = set(h.id for h in all_hosts)
        for arr_h in arrival_hosts_ids:
            if not arr_h in known_hosts_ids:
                transaction.set_rollback(True)
                return {'error': f'Nieznany gospodarz o id: {arr_h}'}, False
        arrival_responsibilities = Responsibility.objects.filter(arrival=arrival_m).all()
        for responsibility in arrival_responsibilities:
            if not responsibility.host in arrival_hosts_ids:
                responsibility.delete()
        for arr_host_id in arrival_hosts_ids:
            found = False
            for responsibility in arrival_responsibilities:
                if arr_host_id == responsibility.host:
                    found = True
            if not found:
                Responsibility(
                    host=arr_host_id,
                    arrival=arrival_m
                ).save()
        arrival_m.save()
        return {'message': f'Wizyta o id: {arrival_m.id} pomyślnie zaktualizowana'}, True

    @transaction.atomic
    def delete_arrival(self, arrival_id: int):
        try:
            to_delete_arr = self.not_confirmed_guests.get(arrival_id=arrival_id).arrival
            to_delete_resp_list = Responsibility.objects.filter(arrival_id=arrival_id).all()
        except ObjectDoesNotExist:
            return {'error': f'Brak niepotwierdzonych spotkań o id: {arrival_id}'}, False
        for resp in to_delete_resp_list:
            resp.delete()
        to_delete_arr.delete()
        return {'message': f'Wizyta o id: {arrival_id} usunięta pomyślnie'}, True


class HostActiveGuestsService:
    def __init__(self, user_id):
        self.user_id = user_id
        self.active_arrivals = (Arrival.objects
                                .filter(Q(leave_timestamp=None) & Q(confirmed=True))
                                .filter(responsibility__host=user_id)
                                .select_related('guest', 'car', 'company')
                                .prefetch_related('responsibility_set')
                                .distinct()
                                )

    def get_active_guests(self):
        full_hosts, success = hosts_API.get_all_hosts_data()
        if not success:
            return full_hosts, success
        full_hosts = full_hosts['message']

        result = []
        for arrival in self.active_arrivals:
            host_ids = [r.host for r in arrival.responsibility_set.all()]
            hosts = []
            for host_id in host_ids:
                host = next((h for h in full_hosts if h.id == host_id), None)
                if host:
                    hosts.append({'name': f"{host.firstname} {host.lastname}"})

            result.append({
                'id': arrival.id,
                'name': f"{arrival.guest.firstname} {arrival.guest.lastname}",
                'company': arrival.company.name if arrival.company else None,
                'register_number': arrival.car.register_number if arrival.car else None,
                'arrival_timestamp': arrival.arrival_timestamp.isoformat(),
                'description': arrival.arrival_purpose,
                'hosts': hosts
            })

        return {'message': result}, True


class HostGuestsHistoryService:
    def __init__(self, user_id):
        self.user_id = user_id
        self.archive_arrivals = (Arrival.objects
                                 .exclude(leave_timestamp=None)
                                 .filter(responsibility__host=user_id)
                                 .select_related('guest', 'car', 'company')
                                 .prefetch_related('responsibility_set')
                                 .distinct()
                                 )

    def get_guests_history(self):
        full_hosts, success = hosts_API.get_all_hosts_data()
        if not success:
            return full_hosts, success
        full_hosts = full_hosts['message']

        result = []
        for arrival in self.archive_arrivals:
            host_ids = [r.host for r in arrival.responsibility_set.all()]
            hosts = []
            for host_id in host_ids:
                host = next((h for h in full_hosts if h.id == host_id), None)
                if host:
                    hosts.append({'name': f"{host.firstname} {host.lastname}"})

            result.append({
                'id': arrival.id,
                'name': f"{arrival.guest.firstname} {arrival.guest.lastname}",
                'company': arrival.company.name if arrival.company else None,
                'register_number': arrival.car.register_number if arrival.car else None,
                'arrival_timestamp': arrival.arrival_timestamp.isoformat(),
                'leave_timestamp': arrival.leave_timestamp.isoformat(),
                'description': arrival.arrival_purpose,
                'hosts': hosts
            })

        return {'message': result}, True
