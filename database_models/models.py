from django.db import models
from daicel_guests_management_system.constants import *
from .model_managers import MeetingManager
from dataclasses import dataclass
from django.core.cache import caches
from hosts_API import functionalities as hosts_API


CACHE = caches['default']

class Company(models.Model):
    name = models.CharField(max_length=30, unique=True)

    class Meta:
        db_table = "Companies"
        
    def __str__(self):
        return self.name

class Guest(models.Model):
    firstname = models.CharField(max_length=30)
    lastname = models.CharField(max_length=30)

    class Meta:
        db_table = "Guests"

    def __str__(self):
        return f"{self.firstname} {self.lastname}"

# class Host(models.Model):
#     class Meta:
#         db_table = "Hosts"

#     def __str__(self):
#         return f"Host {self.id}"
# class HostManager(models.Manager):
#     cache_key = 'cached-hosts'
#     cache_sentinel = object()
#     cache_timeout = 60 * 10

#     def get_queryset(self):
#         # hosts_API.get_all_hosts_data()
#         hosts = CACHE.get(self.cache_key, self.cache_sentinel)
#         if hosts is self.cache_sentinel:
#             data, success = hosts_API.get_all_hosts_data()



class Car(models.Model):
    register_number = models.CharField(max_length=10, unique=True)

    class Meta:
        db_table = "Cars"

    def __str__(self):
        return self.register_number
    
    @classmethod
    def validate_register_number(cls, register_nb):
        # TODO
        return True


class Meeting(models.Model):
    author = models.IntegerField()
    description = models.TextField()
    start_timestamp = models.DateTimeField(auto_now_add=True)
    end_timestamp = models.DateTimeField()

    objects = MeetingManager()

    class Meta:
        db_table = "Meetings"

    def __str__(self):
        return f'{self.author}; {self.start_timestamp.strftime(DATETIME_FORMAT)}-{self.end_timestamp.strftime(DATETIME_FORMAT)}; {self.description}'

class Arrival(models.Model):
    guest = models.ForeignKey(Guest, on_delete=models.RESTRICT)
    car = models.ForeignKey(Car, on_delete=models.RESTRICT)
    arrival_purpose = models.TextField()
    arrival_timestamp = models.DateTimeField(auto_now_add=True)
    leave_timestamp = models.DateTimeField(null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.RESTRICT, null=True, blank=True)

    class Meta:
        db_table = "Arrivals"

    def __str__(self):
        return f"{str(self.guest)}{"; " + str(self.car) if self.car != None else ""}; {self.arrival_timestamp.strftime(DATETIME_FORMAT)}{"; " + self.leave_timestamp.strftime(DATETIME_FORMAT) if self.leave_timestamp else ""}; {self.arrival_purpose}"


class Participation(models.Model):
    arrival = models.ForeignKey(Arrival, on_delete=models.RESTRICT)
    meeting = models.ForeignKey(Meeting, on_delete=models.RESTRICT)

    class Meta:
        db_table = "Participations"
        unique_together = ('arrival', 'meeting')

    def __str__(self):
        return f"Participation: {str(self.arrival)} in {str(self.meeting)}"


class Leadership(models.Model):
    #host = models.ForeignKey(Host, on_delete=models.RESTRICT)
    host = models.IntegerField()
    meeting = models.ForeignKey(Meeting, on_delete=models.RESTRICT)

    class Meta:
        db_table = "Leaderships"
        unique_together = ('host', 'meeting')

    def __str__(self):
        return f"Leadership: {self.host} in {str(self.meeting)}"

class Responsibility(models.Model):
    #host = models.ForeignKey(Host, on_delete=models.RESTRICT)
    host = models.IntegerField()
    arrival = models.ForeignKey(Arrival, on_delete=models.RESTRICT)

    class Meta:
        db_table = "Responsibilities"
        unique_together = ('host', 'arrival')

    def __str__(self):
        return f"Responsibility: {self.host} for {str(self.arrival)}"
