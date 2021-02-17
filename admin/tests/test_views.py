'''
This module contains tests checking views in admin app
'''

from django.test import TestCase
from django.urls import reverse
from study_base.models import StudentGroup
from .utils import (create_admin_user, create_test_user, test_credentials,
    admin_credentials, create_student_group, create_student_users,
    create_teacher_user)


class MainPageViewTests(TestCase):
    '''
    Tests checking main page functionality
    '''

    def setUp(self):
        create_test_user()
        create_admin_user()

        self.url = reverse('admin:admin')

    def test_main_page_get_no_login(self):
        '''
        If user not authenticated, he is redirected to login page
        '''
        response = self.client.get(self.url)
        self.assertRedirects(
            response,
            reverse('auth_base:login') + '?next=' + self.url
        )

    def test_main_page_get_no_admin_login(self):
        '''
        If user is not staff, he is redirected to login page
        '''
        self.client.login(**test_credentials)
        response = self.client.get(self.url)
        self.assertRedirects(
            response,
            reverse('auth_base:login') + '?next=' + self.url
        )

    def test_main_page_get_admin_login(self):
        '''
        If user is staff, main page is shown
        '''
        self.client.login(**admin_credentials)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "admin/admin.html")

class UserDetailsViewTests(TestCase):
    '''
    Tests checking user_details page
    '''

    def setUp(self):
        test_user = create_test_user()
        create_admin_user()

        self.url = reverse('admin:user_detail', args = [test_user.id])
        self.test_user = test_user

    def test_user_details_get_no_login(self):
        '''
        If user not authenticated, he is redirected to login page
        '''
        response = self.client.get(self.url)
        self.assertRedirects(
            response,
            reverse('auth_base:login') + '?next=' + self.url
        )

    def test_user_details_get_no_admin_login(self):
        '''
        If user is not staff, he is redirected to login page
        '''
        self.client.login(**test_credentials)
        response = self.client.get(self.url)
        self.assertRedirects(
            response,
            reverse('auth_base:login') + '?next=' + self.url
        )

    def test_user_details_get_admin_login(self):
        '''
        If user is staff, user_details page is shown
        '''
        self.client.login(**admin_credentials)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "admin/user_details.html")

    def test_user_details_admin_change_user_role(self):
        '''
        Tests changing user role
        '''
        self.client.login(**admin_credentials)
        self.client.post(self.url,{
            'role':'Student'
        })
        self.assertTrue(self.test_user.groups.filter(name = 'Student').exists())

class GroupDetailViewTests(TestCase):
    '''
    Tests group detail view
    '''

    def setUp(self):
        create_test_user()
        create_admin_user()
        test_group = create_student_group()

        self.url = reverse('admin:group_detail', args = [test_group.id])

    def test_group_detail_get_no_login(self):
        '''
        If user not authenticated, he is redirected to login page
        '''
        response = self.client.get(self.url)
        self.assertRedirects(
            response,
            reverse('auth_base:login') + '?next=' + self.url
        )

    def test_group_detail_get_no_admin_login(self):
        '''
        If user is not staff, he is redirected to login page
        '''
        self.client.login(**test_credentials)
        response = self.client.get(self.url)
        self.assertRedirects(
            response,
            reverse('auth_base:login') + '?next=' + self.url
        )

    def test_group_detail_get_admin_login(self):
        '''
        If user is staff, group_detail page is shown
        '''
        self.client.login(**admin_credentials)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "admin/group_detail.html")

class UserListViewTests(TestCase):
    '''
    Tests user list view
    '''

    def setUp(self):
        create_test_user()
        create_admin_user()

        self.url = reverse('admin:user_list')

    def test_user_list_get_no_login(self):
        '''
        If user not authenticated, he is redirected to login page
        '''
        response = self.client.get(self.url)
        self.assertRedirects(
            response,
            reverse('auth_base:login') + '?next=' + self.url
        )

    def test_user_list_get_no_admin_login(self):
        '''
        If user is not staff, he is redirected to login page
        '''
        self.client.login(**test_credentials)
        response = self.client.get(self.url)
        self.assertRedirects(
            response,
            reverse('auth_base:login') + '?next=' + self.url
        )

    def test_user_list_get_admin_login(self):
        '''
        If user is staff, user_list page is shown
        '''
        self.client.login(**admin_credentials)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "admin/user_list.html")

class GroupListViewTests(TestCase):
    '''
    Tests group list view
    '''

    def setUp(self):
        create_test_user()
        create_admin_user()

        self.url = reverse('admin:group_list')

    def test_group_list_get_no_login(self):
        '''
        If user not authenticated, he is redirected to login page
        '''
        response = self.client.get(self.url)
        self.assertRedirects(
            response,
            reverse('auth_base:login') + '?next=' + self.url
        )

    def test_group_list_get_no_admin_login(self):
        '''
        If user is not staff, he is redirected to login page
        '''
        self.client.login(**test_credentials)
        response = self.client.get(self.url)
        self.assertRedirects(
            response,
            reverse('auth_base:login') + '?next=' + self.url
        )

    def test_group_list_get_admin_login(self):
        '''
        If user is staff, group_list page is shown
        '''
        self.client.login(**admin_credentials)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "admin/group_list.html")

class StudentGroupCreateViewTests(TestCase):
    '''
    Tests student group creation
    '''

    def setUp(self):
        teacher = create_teacher_user()
        create_test_user()
        create_admin_user()
        students = create_student_users()

        self.url = reverse('admin:create_group_form')
        self.teacher = teacher.pk
        self.students = [i.pk for i in students]

    def test_group_create_get_no_login(self):
        '''
        If user not authenticated, he is redirected to login page
        '''
        response = self.client.get(self.url)
        self.assertRedirects(
            response,
            reverse('auth_base:login') + '?next=' + self.url
        )

    def test_group_create_get_no_admin_login(self):
        '''
        If user is not staff, he is redirected to login page
        '''
        self.client.login(**test_credentials)
        response = self.client.get(self.url)
        self.assertRedirects(
            response,
            reverse('auth_base:login') + '?next=' + self.url
        )

    def test_group_create_get_admin_login(self):
        '''
        If user is staff, group_create page is shown
        '''
        self.client.login(**admin_credentials)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "admin/group_form.html")

    def test_new_group_post_creates_new_group(self):
        '''
        Checks if new group creates after correct POST request
        '''
        self.client.login(**admin_credentials)
        response = self.client.post(self.url, {
            'name':'TestGroup Name',
            'teacher':self.teacher,
            'students':self.students
        })
        self.assertRedirects(response,reverse('admin:group_list'))
        self.assertEqual(
            StudentGroup.objects.get(teacher = self.teacher).name,
            "TestGroup Name"
        )

class StudentGroupUpdateViewTests(TestCase):
    '''
    Tests student group update view
    '''

    def setUp(self):
        group = create_student_group()
        create_test_user()
        create_admin_user()

        self.url = reverse('admin:update_group', args = [group.id])
        self.group = group

    def test_group_update_get_no_login(self):
        '''
        If user not authenticated, he is redirected to login page
        '''
        response = self.client.get(self.url)
        self.assertRedirects(
            response,
            reverse('auth_base:login') + '?next=' + self.url
        )

    def test_group_update_get_no_admin_login(self):
        '''
        If user is not staff, he is redirected to login page
        '''
        self.client.login(**test_credentials)
        response = self.client.get(self.url)
        self.assertRedirects(
            response,
            reverse('auth_base:login') + '?next=' + self.url
        )

    def test_group_update_get_admin_login(self):
        '''
        If user is staff, group_update page is shown
        '''
        self.client.login(**admin_credentials)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "admin/group_form.html")

    def test_group_update_post_updates(self):
        '''
        Checks if group updates
        '''
        self.client.login(**admin_credentials)
        response = self.client.post(self.url,{
            'name': 'Test Updated Group',
            'teacher':self.group.teacher.pk,
            'students': [i.pk for i in self.group.students.all()]
        })

        self.assertRedirects(response, reverse('admin:group_list'))
        self.assertEqual(
            StudentGroup.objects.get(id = self.group.id).name,
            'Test Updated Group'
        )
