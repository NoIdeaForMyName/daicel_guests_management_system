from database_models.models import *
from hosts_API.functionalities import *
from datetime import datetime, time
from daicel_guests_management_system.constants import *

'''
1. pobierz dane wszystkich osob odpowiedzialnych
2. pobierz dane wszystkich aktywnych spotkan
3. pobierz dane wszystkich firm
4. pobierz dane wszystkich zarejestrowanych (rowniez historycznie) gości

'''

def get_all_hosts():
    return get_all_hosts_data()

'''
class Meeting(models.Model):
    author = models.IntegerField()
    description = models.TextField()
    start_timestamp = models.DateTimeField(auto_now_add=True)
    end_timestamp = models.DateTimeField()

    class Meta:
        db_table = "Meetings"
'''
def get_active_meetings(from_today=True):
    active_meetings = Meeting.objects.filter(end_timestamp__gt=datetime.now())
    if from_today:
        day_end_datetime = datetime.combine(datetime.now().date(), time(23, 59, 59))
        active_meetings = active_meetings.filter(start_timestamp__lte=day_end_datetime)
    return active_meetings.all()

def get_active_meetings_full_data(from_today=True):
    meetings = get_active_meetings(from_today)
    hosts, success = get_all_hosts()
    if not success:
        return hosts, success
    def meeting_to_str(meeting):
        host_ids = set(Host.objects.filter(leadership__meeting=meeting))
        hosts = filter(lambda h: h.id in host_ids, hosts)
        meeting_date = meeting.start_timestamp.date
        start_time = meeting.start_timestamp.time
        end_time = meeting.end_timestamp.time
        return f'{", ".join(hosts)}{("; " + meeting_date.strftime(DATE_FORMAT)) if not from_today else ''}; {start_time.strftime(TIME_FORMAT)}-{end_time.strftime(TIME_FORMAT)}; {meeting.description}'
    meetings_full = map(meeting_to_str, meetings)
    return {"message": meetings_full}, True