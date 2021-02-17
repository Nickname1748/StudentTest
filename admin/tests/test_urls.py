'''
This module contains tests of URL matching in admin app
'''

from django.test import SimpleTestCase
from django.urls import reverse, resolve
from admin import views

class URLsTests(SimpleTestCase):
    '''
    Tests checking URLs
    '''

    def test_main_view_resolves(self):
        '''
        admin:admin
        '''
        url = reverse('admin:admin')
        self.assertEqual(resolve(url).func.view_class, views.MainView)

    def test_user_list_view_resolves(self):
        '''
        admin:user_list
        '''
        url = reverse('admin:user_list')
        self.assertEqual(resolve(url).func.view_class, views.UserListView)

    def test_user_details_view_resolves(self):
        '''
        admin:user_detail
        '''
        url = reverse('admin:user_detail', args = [1])
        self.assertEqual(resolve(url).func, views.user_details)

    def test_group_detail_view_resolves(self):
        '''
        admin:group_detail
        '''
        url = reverse('admin:group_detail', args = ['123e4567-e89b-12d3-a456-426655440000'])
        self.assertEqual(resolve(url).func.view_class, views.GroupDetailView)

    def test_group_update_view_resolves(self):
        '''
        admin:update_group
        '''
        url = reverse('admin:update_group', args = ['123e4567-e89b-12d3-a456-426655440000'])
        self.assertEqual(resolve(url).func.view_class, views.StudentGroupUpdateView)

    def test_group_list_view_resolves(self):
        '''
        admin:group_list
        '''

        url = reverse('admin:group_list')
        self.assertEqual(resolve(url).func.view_class, views.GroupListView)

    def test_group_create_view_resolves(self):
        '''
        admin:create_group_form
        '''

        url = reverse('admin:create_group_form')
        self.assertEqual(resolve(url).func.view_class, views.StudentGroupCreateView)
