from django.urls import path
from host import views

from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.home, name='host-home'),
    path('my-guests', views.my_guests, name='host-my-guests'),

    path('login/', views.login_host, name='login'),
]
