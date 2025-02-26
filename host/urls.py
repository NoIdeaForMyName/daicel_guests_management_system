from django.urls import path
from host import views

urlpatterns = [
    path('', views.home, name='host-home'),
    path('new-meeting', views.new_meeting, name='host-new-meeting'),
    path('my-guests', views.my_guests, name='host-my-guests'),
    path('my-meetings', views.my_meetings, name='host-my-meetings'),
    path('led-meetings', views.led_meetings, name='host-led-meetings'),
]
