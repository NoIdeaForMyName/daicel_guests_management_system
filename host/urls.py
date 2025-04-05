from django.urls import path
from host import views
from add_guest.views import add_guest, add_guest_process
from django.contrib.auth.decorators import login_required


from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.home, name='host-home'),
    path('add-guest', login_required(add_guest, login_url="/host/login/"), {"src": "host"}, name='host-add-guest'),
    path('add-guest-process', login_required(add_guest_process, login_url="/host/login/"), name='host-add-guest-process'),
    path('my-guests', views.my_guests, name='host-my-guests'),
    path('not-confirmed-guests', views.not_confirmed_guests, name='host-not-confirmed-guests'),
    path('active-guests', views.active_guests, name='host-active-guests'),
    path('guests-history', views.guests_history, name='host-guests-history'),
    path('edit_guest/<int:arrival_id>/', views.edit_guest, name='host-edit-guest'),

    path('login/', views.login_host, name='login'),
]
