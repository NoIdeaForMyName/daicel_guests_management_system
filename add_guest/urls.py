from django.urls import path
from . import views

urlpatterns = [
    path('', views.add_guest, name='add-guest'),
]
