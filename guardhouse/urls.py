from django.urls import path
from guardhouse import views

urlpatterns = [
    path('', views.home, name='guardhouse-home'),
    path('add-guest', views.add_guest, name='guardhouse-add-guest'),
    path('active-guests', views.active_guests, name='guardhouse-active-guests'),
    path('guests-history', views.guests_history, name='guardhouse-guests-history'),
    path('add-guest-process', views.add_guest_process, name='guardhouse-add-guest-process'),
]
