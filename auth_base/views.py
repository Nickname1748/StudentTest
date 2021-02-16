# Student Test System
# Copyright (C) 2020-2021 Andrey Shmaykhel <shmayhel.andrey@gmail.com>,
#                         Alexander Solovyov
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""
This module contains auth_base views
"""

from django.shortcuts import redirect
from django_registration.backends.activation.views import RegistrationView
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from .forms import RegisterForm


@login_required
def index_view(request):
    """
    Index page.
    """
    if request.user.is_staff:
        return redirect('admin:admin')
    return redirect('study_base:index')


class RegisterView(RegistrationView):
    """
    Registration view class.
    """
    form_class = RegisterForm
    success_url = reverse_lazy('auth_base:registration_complete')
    disallowed_url = reverse_lazy('auth_base:registration_disallowed')

    def create_inactive_user(self, form):
        new_user = super().create_inactive_user(form)
        group = Group.objects.get_or_create(name="Unknown")[0]
        new_user.groups.add(group)
        new_user.save()

        return new_user
