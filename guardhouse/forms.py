from django import forms

class GuestForm(forms.Form):
    company = forms.CharField(label="Nazwa firmy", max_length=30)

class PersonalDataForm(forms.Form):
    last_name = forms.CharField(label="Nazwisko", max_length=30)
    first_name = forms.CharField(label="Imię", max_length=30)

