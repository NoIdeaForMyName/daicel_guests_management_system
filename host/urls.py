from django.urls import path
from host import views
from add_guest.views import add_guest, add_guest_process
from django.contrib.auth.decorators import login_required


from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.home, name='host-home'),
    path('add-guest', login_required(add_guest, login_url="/host/login/"), {"confirmed": False, "process_url": "/host/add-guest-process"}, name='host-add-guest'),
    path('add-guest-process', login_required(add_guest_process, login_url="/host/login/"), name='host-add-guest-process'),
    path('my-guests', views.my_guests, name='host-my-guests'),

    path('login/', views.login_host, name='login'),
]
