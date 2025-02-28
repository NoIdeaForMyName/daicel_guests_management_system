from database_models.models import *
import hosts_API.functionalities as hosts_API
from datetime import datetime, time
from daicel_guests_management_system.constants import *
from django.db import transaction
from django.forms.models import model_to_dict
from django.db.models import Q


class ActiveGuestsService:

    def __init__(self):
        self.active_arrivals = (Arrival.objects
                                .filter(leave_timestamp=None)
                                .filter(confirmed=True)
                                .select_related('guest')
                                .select_related('car')
                                .select_related('company')
                                .prefetch_related('responsibility_set')
                                .all()
                                )
        print("LOLZ:", self.active_arrivals.values())

    def all_cars_at_workplace(self) -> int:
        return self.active_arrivals.filter(~Q(car=None)).values('car').distinct().count()

    def active_guests_count(self) -> int:
        return self.active_arrivals.all().count()

    def active_arrivals_context(self) -> tuple[dict, bool]:
        full_hosts, success = hosts_API.get_all_hosts_data()
        if not success:
            return full_hosts, success
        full_hosts = full_hosts['message']
        return {'message': 
            [
                {
                    'id': arrival.id,
                    'name': f'{arrival.guest.firstname} {arrival.guest.lastname}',
                    'company': arrival.company.name if arrival.company else None,
                    'register_number': arrival.car.register_number if arrival.car else None,
                    'arrival_timestamp': arrival.arrival_timestamp.strftime(DATETIME_FORMAT),
                    'description': arrival.arrival_purpose,
                    'hosts': [
                        {
                            'name': f'{host.firstname} {host.lastname}'
                        }
                        for host in [h for h in full_hosts if h.id in map(lambda r: r['host'], arrival.responsibility_set.all().values('host'))]
                    ]
                }
                for arrival in self.active_arrivals
            ]
        }, True
    
    def end_arrivals(self, ids):
        arrivals = Arrival.objects.filter(id__in=ids).all()
        for arrival in arrivals:
            arrival.leave_timestamp = datetime.now()
            arrival.save()


class GuestsHistoryService:

    def __init__(self):
        self.archive_arrivals = (Arrival.objects
                                 .filter(~Q(leave_timestamp=None))
                                 .select_related('guest')
                                 .select_related('car')
                                 .select_related('company')
                                 .prefetch_related('responsibility_set')
                                 .all()
                                )

    def archive_arrivals_context(self):
        full_hosts, success = hosts_API.get_all_hosts_data()
        if not success:
            return full_hosts, success
        full_hosts = full_hosts['message']
        return {'message': 
            [
                {
                    'id': arrival.id,
                    'name': f'{arrival.guest.firstname} {arrival.guest.lastname}',
                    'company': arrival.company.name if arrival.company else None,
                    'register_number': arrival.car.register_number if arrival.car else None,
                    'arrival_timestamp': arrival.arrival_timestamp.strftime(DATETIME_FORMAT),
                    'leave_timestamp': arrival.leave_timestamp.strftime(DATETIME_FORMAT),
                    'description': arrival.arrival_purpose,
                    'hosts': [
                        {
                            'name': f'{host.firstname} {host.lastname}'
                        }
                        for host in [h for h in full_hosts if h.id in map(lambda r: r['host'], arrival.responsibility_set.all().values('host'))]
                    ]
                }
                for arrival in self.archive_arrivals
            ]
        }, True


class NotConfirmedArrivalsService:

    def __init__(self):
        self.not_confirmed_arrivals = (Arrival.objects
                                        .filter(confirmed=False)
                                        .select_related('guest')
                                        .select_related('car')
                                        .select_related('company')
                                        .prefetch_related('responsibility_set')
                                        .all()
                                        )

    def not_confirmed_arrivals_context(self):
        full_hosts, success = hosts_API.get_all_hosts_data()
        if not success:
            return full_hosts, success
        full_hosts = full_hosts['message']
        return {'message':
            [
                {
                    'id': arrival.id,
                    'name': f'{arrival.guest.firstname} {arrival.guest.lastname}',
                    'company': arrival.company.name if arrival.company else None,
                    'description': arrival.arrival_purpose,
                    'hosts': [
                        {
                            'name': f'{host.firstname} {host.lastname}'
                        }
                        for host in [h for h in full_hosts if h.id in map(lambda r: r['host'], arrival.responsibility_set.all().values('host'))]
                    ]
                }
                for arrival in self.not_confirmed_arrivals
            ]
        }, True