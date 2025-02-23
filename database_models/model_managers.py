from django.db import models
#from .models import Company, Guest, Car, Meeting, Arrival, Participation, Leadership, Responsibility
from datetime import datetime, time

'''
def __get_active_meetings_models(from_today=True):
    active_meetings = Meeting.objects.filter(end_timestamp__gt=datetime.now())
    if from_today:
        day_end_datetime = datetime.combine(datetime.now().date(), time(23, 59, 59))
        active_meetings = active_meetings.filter(start_timestamp__lte=day_end_datetime)
    return active_meetings.all()
'''

class MeetingManager(models.Manager):
    def get_active(self, from_today=True):
        active_meetings = self.filter(end_timestamp__gt=datetime.now())
        if from_today:
            day_end_datetime = datetime.combine(datetime.now().date(), time(23, 59, 59))
            active_meetings = active_meetings.filter(start_timestamp__lte=day_end_datetime)
        return active_meetings.all()
