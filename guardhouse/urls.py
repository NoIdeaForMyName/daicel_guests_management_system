from django.urls import path
from guardhouse import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add-guest', views.add_guest, name='add-guest'),
    path('active-guests', views.active_guests, name='active-guests'),
    path('guests-history', views.guests_history, name='guests-history'),
    path('add-guest-process', views.add_guest_process, name='add-guest-process'),
]
