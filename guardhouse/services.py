from database_models.models import *
import hosts_API.functionalities as hosts_API
from datetime import datetime, time
from daicel_guests_management_system.constants import *
from django.db import transaction
from django.forms.models import model_to_dict


'''
1. pobierz dane wszystkich osob odpowiedzialnych DONE
2. pobierz dane wszystkich aktywnych spotkan DONE
3. pobierz dane wszystkich firm
4. pobierz dane wszystkich zarejestrowanych (rowniez historycznie) gości

'''


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
        meetings = data['meetings']

        company_m = None
        car_m = None
        guests_m = []
        meetings_m = []
        arrivals_m = []
        hosts_m_API = []

        all_hosts, success = hosts_API.get_all_hosts_data()
        if not success:
            return all_hosts, success
        all_hosts = set(all_hosts['message'])

        if company_name:
            company_m = Company.objects.filter(name=company_name).first()
            if company_m == None:
                company_m = Company(name=company_name)
                company_m.save()
        
        if not Car.validate_register_number(register_nb):
            transaction.set_rollback(True)
            return {'error': f"Incorrect register number {register_nb}"}, False
        car_m = Car.objects.filter(register_number=register_nb).first()
        if car_m == None:
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
            
        # 'meetings': [{'id': '2', 'start_time': '08:31', 'end_time': '15:00', 'date': '02/19/2025', 'description': 'Vivamus malesuada elementum, maecenas molestie ...'}]
        for meeting in meetings:
            meeting_m = Meeting.objects.filter(id=meeting['id']).first()
            if meeting_m == None:
                transaction.set_rollback(True)
                return {'error': f"Provided meeting: {meeting} is incorrect"}, False
            meetings_m.append(meeting_m)

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
                guest = guest_m,
                car = car_m,
                arrival_purpose = description,
                #arrival_timestamp = datetime.now(),
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

            for meeting_m in meetings_m:
                participation_m = Participation(
                    arrival = arrival_m,
                    meeting = meeting_m
                )
                participation_m.save()

        return {'message': f"Arrivals added succesfully: {data}"}, True


class MeetingService:
    @classmethod
    def get_active_meetings_full_data(from_today=True):
        meetings = Meeting.objects.get_active(from_today)
        def meeting_to_dict(meeting):
            hosts_set = set(map(lambda leadership: leadership.host, Leadership.objects.filter(meeting=meeting)))
            full_hosts, success = hosts_API.get_all_hosts_data()
            if not success:
                return full_hosts, success
            full_hosts_filtered = list(filter(lambda h: h.id in hosts_set, full_hosts['message']))
            meeting_date = meeting.start_timestamp.date()
            start_time = meeting.start_timestamp.time()
            end_time = meeting.end_timestamp.time()
            return {
                'id': meeting.id,
                'leaders': [host.to_dict for host in full_hosts_filtered],
                'date': meeting_date.strftime(DATE_FORMAT),
                'start_time': start_time.strftime(TIME_FORMAT),
                'end_time': end_time.strftime(TIME_FORMAT),
                'description': meeting.description
            }
        meetings_full = list(map(meeting_to_dict, meetings))
        return {"message": meetings_full}, True
