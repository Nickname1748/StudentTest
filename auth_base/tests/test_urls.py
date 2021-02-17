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
This module contains tests of URL matching in auth_base app
'''

from django_registration.backends.activation import views as registration_views

from django.test import SimpleTestCase
from django.urls import reverse, resolve
from django.contrib.auth import views as auth_views

from auth_base import views

class AuthURLsTests(SimpleTestCase):
    '''
    Tests checking auth URLs
    '''

    def test_login_view_resolves(self):
        '''
        auth_base:login
        '''
        url = reverse('auth_base:login')
        self.assertEqual(resolve(url).func.view_class, auth_views.LoginView)

    def test_logout_view_resolves(self):
        '''
        auth_base:logout
        '''
        url = reverse('auth_base:logout')
        self.assertEqual(resolve(url).func.view_class, auth_views.LogoutView)

class RegistrationURLsTests(SimpleTestCase):
    '''
    Tests checking registration URLs
    '''

    def test_activate_view_resolves(self):
        '''
        auth_base:activate
        '''
        url = reverse(
            'auth_base:activate',
            args=[
                'IoelYjQi:1kckPR:JHTTCehMd752yaNJyMJY4oChloxBCkd7hxKepVbjtR4'
            ])
        self.assertEqual(
            resolve(url).func.view_class, registration_views.ActivationView
        )

    def test_register_view_resolves(self):
        '''
        auth_base:register
        '''
        url = reverse('auth_base:register')
        self.assertEqual(resolve(url).func.view_class, views.RegisterView)
