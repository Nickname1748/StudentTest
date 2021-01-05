from django.shortcuts import render
from django_registration.backends.activation.views import (
    RegistrationView, ActivationView)
from django.contrib.auth.models import Group
from .forms import RegisterForm
from django.urls import reverse_lazy

# Create your views here.
class RegisterView(RegistrationView):
    form_class = RegisterForm
    success_url = reverse_lazy('auth_base:registration_complete')
    disallowed_url = reverse_lazy('auth_base:registration_disallowed')

    def create_inactive_user(self, form):
        new_user = super().create_inactive_user(form)
        group = Group.objects.get_or_create(name="Unknown")[0]
        new_user.groups.add(group)
        new_user.save()

        return new_user