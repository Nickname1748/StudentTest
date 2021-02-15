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
