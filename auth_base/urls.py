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

'''
This module contains auth_base views
'''

from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView
from django_registration.backends.activation import views as registration_views
from . import views

app_name = 'auth_base'

urlpatterns = [
    path('', views.index_view, name='index'),
    path('login/', auth_views.LoginView.as_view(), name = 'login'),
    path('logout/', auth_views.LogoutView.as_view(), name = 'logout'),
    path('register/', views.RegisterView.as_view(), name = 'register'),
    path(
        "activate/complete/",
        TemplateView.as_view(
            template_name = "django_registration/activation_complete.html"
        ),
        name = "activation_complete"
    ),
    path(
        "activate/<str:activation_key>/",
        registration_views.ActivationView.as_view(
            success_url = reverse_lazy('auth_base:activation_complete')
        ),
        name = "activate"
    ),
    path(
        "register/complete/",
        TemplateView.as_view(
            template_name = 'django_registration/registration_complete.html'
        ),
        name="registration_complete"
    ),
    path(
        "register/closed/",
        TemplateView.as_view(
            template_name="django_registration/registration_closed.html"
        ),
        name="registration_disallowed"
    ),
]
