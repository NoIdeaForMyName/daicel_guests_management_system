from django.urls import path, include
from guardhouse import views
from add_guest.views import add_guest, add_guest_process
from .security import validate_ip

urlpatterns = [
    path('', views.home, name='guardhouse-home'),
    path('add-guest', validate_ip(add_guest), {"confirmed": True, "process_url": "/guardhouse/add-guest-process"}, name='guardhouse-add-guest'),
    path('add-guest-process', validate_ip(add_guest_process), name='guardhouse-add-guest-process'),
    path('active-guests', views.active_guests, name='guardhouse-active-guests'),
    path('guests-history', views.guests_history, name='guardhouse-guests-history'),
]
