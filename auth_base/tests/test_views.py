# Student Test System
# Copyright (C) 2020 Andrey Shmaykhel <shmayhel.andrey@gmail.com>,
#                    Alexander Solovyov
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
This modules containes tests checking auth_base views
'''

from django.test import TestCase
from django.urls import reverse
from .utils import check_user_in_group

class RegisterTestViews(TestCase):
    '''
    Tests checking register views
    '''

    def setUp(self):
        self.url = reverse('auth_base:register')

    def test_register_view_get(self):
        '''
        Testing GET request response
        '''
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'django_registration/registration_form.html')

    def test_register_post(self):
        '''
        Testing POST request response
        '''
        response = self.client.post(self.url,
        {
            'username':'donaldtrump',
            'first_name':'Donald',
            'last_name':'Trump',
            'email':'donaldtrump@gmail.com',
            'password1':'maga2020!',
            'password2':'maga2020!'
        })
        self.assertRedirects(response, reverse('auth_base:registration_complete'))
        self.assertTrue(check_user_in_group('donaldtrump', 'Unknown'))

    def test_registration_failes(self):
        '''
        Testing wrong POST request to fail
        '''
        response = self.client.post(self.url,{})
        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(response.context['form'].errors), 0)
