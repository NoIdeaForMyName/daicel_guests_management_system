from datetime import datetime
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
                'arrival_timestamp': arrival.arrival_timestamp.strftime(DATETIME_FORMAT),
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
                'arrival_timestamp': arrival.arrival_timestamp.strftime(DATETIME_FORMAT),
                'leave_timestamp': arrival.leave_timestamp.strftime(DATETIME_FORMAT),
                'description': arrival.arrival_purpose,
                'hosts': hosts
            })

        return {'message': result}, True
