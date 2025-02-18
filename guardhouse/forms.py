from django import forms
from django.forms import formset_factory, ModelForm, inlineformset_factory
from database_models.models import *


class GuestForm(ModelForm):
    class Meta:
        model = Guest
        fields = ["firstname", "lastname"]
    # last_name = forms.CharField(label="Nazwisko", max_length=30)
    # first_name = forms.CharField(label="Imię", max_length=30)

GuestFormset = formset_factory(GuestForm)

class CollectiveGuestsDataForm(forms.Form):
    company = forms.CharField(label="Nazwa firmy", max_length=30)
    register_nb = forms.CharField(label="Numer rejestracyjny (opcjonalnie)", max_length=10)
    arrival_purpose = forms.CharField(widget=forms.Textarea, label="Cel przybycia")

class HostForm(forms.Form):
    id = forms.IntegerField()
    firstname = forms.CharField(max_length=30)
    lastname = forms.CharField(max_length=30)
