from django import forms
from django.contrib.auth.models import User


class EditProfile(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')


class AuthCodeForm(forms.Form):
    code = forms.IntegerField(label="Код регистрации")

