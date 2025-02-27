from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(label="Nazwa użytkownika", max_length=100)
    password = forms.CharField(label="Hasło", widget=forms.PasswordInput())
    next = forms.CharField()
