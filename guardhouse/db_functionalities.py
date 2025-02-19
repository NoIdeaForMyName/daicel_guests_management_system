from database_models.models import *
import hosts_API.functionalities as hosts_API
from datetime import datetime, time
from daicel_guests_management_system.constants import *
from django.forms.models import model_to_dict


'''
1. pobierz dane wszystkich osob odpowiedzialnych DONE
2. pobierz dane wszystkich aktywnych spotkan DONE
3. pobierz dane wszystkich firm
4. pobierz dane wszystkich zarejestrowanych (rowniez historycznie) gości

'''

def add_new_arrival_data(data):
    # TODO
    print("DATA:", data)

def get_all_companies():
    return list(Company.objects.all().values())

def get_all_known_guests():
    return [__guest_to_dict(guest) for guest in Guest.objects.all()]

def __guest_to_dict(guest):
    return {
        "id": guest.id,
        "firstname": guest.firstname,
        "lastname": guest.lastname,
        "company": Company.objects.filter(id=guest.company_id).values()[0]
    }


def __get_active_meetings_models(from_today=True):
    active_meetings = Meeting.objects.filter(end_timestamp__gt=datetime.now())
    if from_today:
        day_end_datetime = datetime.combine(datetime.now().date(), time(23, 59, 59))
        active_meetings = active_meetings.filter(start_timestamp__lte=day_end_datetime)
    return active_meetings.all()

def get_all_hosts():
    full_hosts, success = hosts_API.get_all_hosts_data()
    if not success:
        return full_hosts, success
    return {'message': [__full_host_to_dict(host) for host in full_hosts['message']]}, True

def __full_host_to_dict(host):
    return {"id": host.id, "firstname": host.firstname, "lastname": host.lastname}

def get_active_meetings(from_today=True):
    return __get_active_meetings_models(from_today).values()

def get_active_meetings_full_data(from_today=True):
    meetings = __get_active_meetings_models(from_today)
    hosts, success = get_all_hosts()
    if not success:
        return hosts, success
    def meeting_to_dict(meeting):
        hosts_set = set(map(lambda host: host.id, Host.objects.filter(leadership__meeting=meeting)))
        full_hosts, success = hosts_API.get_all_hosts_data()
        if not success:
            return full_hosts, success
        full_hosts_filtered = list(filter(lambda h: h.id in hosts_set, full_hosts['message']))
        meeting_date = meeting.start_timestamp.date()
        start_time = meeting.start_timestamp.time()
        end_time = meeting.end_timestamp.time()
        return {
            'id': meeting.id,
            'leaders': [__full_host_to_dict(host) for host in full_hosts_filtered],
            'date': meeting_date.strftime(DATE_FORMAT),
            'start_time': start_time.strftime(TIME_FORMAT),
            'end_time': end_time.strftime(TIME_FORMAT),
            'description': meeting.description
        }
        #return f'{", ".join(hosts)}{("; " + meeting_date.strftime(DATE_FORMAT)) if not from_today else ''}; {start_time.strftime(TIME_FORMAT)}-{end_time.strftime(TIME_FORMAT)}; {meeting.description}'
    #print("SADADADD",meetings[0].start_timestamp.time().strftime(TIME_FORMAT))
    meetings_full = list(map(meeting_to_dict, meetings))
    return {"message": meetings_full}, True
