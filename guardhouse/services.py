from database_models.models import *
import hosts_API.functionalities as hosts_API
from datetime import datetime, time
from daicel_guests_management_system.constants import *
from django.db import transaction
from django.forms.models import model_to_dict
from django.db.models import Q


class HostNewGuestsService:

    @staticmethod
    @transaction.atomic
    def add_new_arrival_data(data):

        print("JSON:", data)

        company_name = data['company']
        register_nb = data['register_number']
        guests = data['guests']
        description = data['description']
        hosts = data['hosts']

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
            #host_m_API = [host for host in all_hosts if (host.id, host.firstname, host.lastname) == (host_API['id'], host_API['firstname'], host_API['lastname'])]
            #host_m_API = None if host_m_API == [] else host_m_API
            host_m_API = hosts_API.FullHost(**host_API)
            if not host_m_API in all_hosts:
                transaction.set_rollback(True)
                return {'error': f"Given host: {host_API} doesn't exists in the database"}, False
            hosts_m_API.append(host_m_API)

        for guest_m in guests_m:
            arrival_m = Arrival(
                confirmed = True,
                guest = guest_m,
                arrival_purpose = description,
                car = car_m,
                arrival_timestamp = datetime.now(),
                company = company_m
            )
            arrival_m.save()
            arrivals_m.append(arrival_m)

            for host_m_API in hosts_m_API:
                responsibility_m = Responsibility(
                    host = host_m_API.id,
                    arrival = arrival_m
                )
                responsibility_m.save()

            arrival_m.save()

        return {'message': f"Arrivals added succesfully: {data}"}, True


class ActiveGuestsService:

    def __init__(self):
        self.active_arrivals = (Arrival.objects.filter(leave_timestamp=None)
            .select_related('guest')
            .select_related('car')
            .select_related('company')
            .prefetch_related('responsibility_set')
            .all()
        )

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
        self.archive_arrivals = (Arrival.objects.filter(~Q(leave_timestamp=None))
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
