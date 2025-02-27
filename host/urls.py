from django.urls import path
from host import views

from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.home, name='host-home'),
    path('add-meeting', views.add_meeting, name='host-add-meeting'),
    path('add-meeting-process', views.add_meeting_process, name='host-add-meeting-process'),
    path('my-guests', views.my_guests, name='host-my-guests'),
    path('my-meetings', views.my_meetings, name='host-my-meetings'),
    path('led-meetings', views.led_meetings, name='host-led-meetings'),

    path('login/', views.login_host, name='login'),
]
