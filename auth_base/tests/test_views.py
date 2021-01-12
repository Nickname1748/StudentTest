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
