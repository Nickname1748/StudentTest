'''
This module contains auth_base forms
'''

from django_registration.forms import RegistrationForm
from django import forms
from django.contrib.auth import get_user_model

class RegisterForm(RegistrationForm):
    '''
    Registration form
    '''
    first_name = forms.CharField(max_length=30, label=("First name"))
    last_name = forms.CharField(max_length=30, label=("Last name"))
    email = forms.EmailField(label=("Email"))

    class Meta:
        model = get_user_model()
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2'
        ]
