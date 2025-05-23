from django.db import models
from daicel_guests_management_system.constants import *
from dataclasses import dataclass
#from django.core.cache import caches
from hosts_API import functionalities as hosts_API
from django.utils import timezone


#CACHE = caches['default']

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

#     def get_queryset(self):
#         data, success = hosts_API.get_all_hosts_data()
#         if success:
#             data = data['message']
#         else:
#             data = []
        



class Car(models.Model):
    register_number = models.CharField(max_length=10, unique=True)

    class Meta:
        db_table = "Cars"

    def __str__(self):
        return self.register_number
    
    @classmethod
    def validate_register_number(cls, register_nb):
        return len(register_nb) <= MAX_REGISTER_NB_LEN

    def save(self, *args, **kwargs):
        if self.register_number:
            self.register_number = self.register_number.upper()
        super().save(*args, **kwargs)


class Arrival(models.Model):
    confirmed = models.BooleanField()
    guest = models.ForeignKey(Guest, on_delete=models.RESTRICT)
    arrival_purpose = models.TextField()
    car = models.ForeignKey(Car, on_delete=models.RESTRICT, null=True, blank=True)
    arrival_timestamp = models.DateTimeField(null=True, blank=True)
    leave_timestamp = models.DateTimeField(null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.RESTRICT, null=True, blank=True)

    class Meta:
        db_table = "Arrivals"

    def __str__(self):
        return f"{str(self.guest)}{"; " + str(self.car) if self.car != None else ""}{"; " + timezone.localtime(self.arrival_timestamp).isoformat() if self.arrival_timestamp != None else ""}{"; " + self.leave_timestamp.strftime(DATETIME_FORMAT) if self.leave_timestamp else ""}; {self.arrival_purpose}"


class Responsibility(models.Model):
    #host = models.ForeignKey(Host, on_delete=models.RESTRICT)
    host = models.IntegerField()
    arrival = models.ForeignKey(Arrival, on_delete=models.RESTRICT)

    class Meta:
        db_table = "Responsibilities"
        unique_together = ('host', 'arrival')

    def __str__(self):
        return f"Responsibility: {self.host} for {str(self.arrival)}"
