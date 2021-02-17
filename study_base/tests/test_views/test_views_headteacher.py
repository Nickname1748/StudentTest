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
This module containes tests checking study_base headteacher views.
'''

from django.test import TestCase
from django.urls import reverse

from study_base.tests.utils import create_student_group, create_test_module, create_test_task, create_teacher_user, test_credentials, create_test_user, headteacher_credentials, create_headteacher_user


class HeadteacherHomeViewTests(TestCase):
    """
    Tests checking headteacher home view functionality.
    """

    def setUp(self):
        create_headteacher_user()
        create_test_user()

        self.url = reverse('study_base:headteacher_home')

    def test_headteacher_home_view_get_no_login(self):
        """
        If user is not authenticated, he is redirected to login page.
        """
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse('auth_base:login') + '?next=' + self.url)

    def test_headteacher_home_view_get_login_not_headteacher(self):
        """
        If user is not headteacher, he is redirected to login page.
        """
        self.client.login(**test_credentials)
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse('auth_base:login') + '?next=' + self.url)

    def test_headteacher_home_view_get_login_headteacher(self):
        """
        If user is headteacher, headteacher home view is shown.
        """
        self.client.login(**headteacher_credentials)
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'study_base/headteacher_home.html')


class HeadGroupDetailViewTests(TestCase):
    """
    Tests checking headteacher group detail view functionality.
    """

    def setUp(self):
        create_headteacher_user()
        create_test_user()

        group = create_student_group()

        self.url = reverse('study_base:group_detail_head', args=[group.id])

    def test_head_group_detail_view_get_no_login(self):
        """
        If user is not authenticated, he is redirected to login page.
        """
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse('auth_base:login') + '?next=' + self.url)

    def test_head_group_detail_view_get_login_not_headteacher(self):
        """
        If user is not headteacher, he is redirected to login page.
        """
        self.client.login(**test_credentials)
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse('auth_base:login') + '?next=' + self.url)

    def test_head_group_detail_view_get_login_headteacher(self):
        """
        If user is headteacher, headteacher group detail view is shown.
        """
        self.client.login(**headteacher_credentials)
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'study_base/group_detail_head.html')


class TeacherDetailViewTests(TestCase):
    """
    Tests checking teacher detail view functionality.
    """

    def setUp(self):
        create_headteacher_user()
        create_test_user()

        teacher = create_teacher_user()

        self.url = reverse('study_base:teacher_detail', args=[teacher.id])

    def test_teacher_detail_view_get_no_login(self):
        """
        If user is not authenticated, he is redirected to login page.
        """
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse('auth_base:login') + '?next=' + self.url)

    def test_teacher_detail_view_get_login_not_headteacher(self):
        """
        If user is not headteacher, he is redirected to login page.
        """
        self.client.login(**test_credentials)
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse('auth_base:login') + '?next=' + self.url)

    def test_teacher_detail_view_get_login_headteacher(self):
        """
        If user is headteacher, teacher detail view is shown.
        """
        self.client.login(**headteacher_credentials)
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'study_base/teacher_detail.html')


class ModuleDetailViewTests(TestCase):
    """
    Tests checking module detail view functionality.
    """

    def setUp(self):
        create_headteacher_user()
        create_test_user()

        module = create_test_module()

        self.url = reverse('study_base:module_detail', args=[module.id])

    def test_module_detail_view_get_no_login(self):
        """
        If user is not authenticated, he is redirected to login page.
        """
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse('auth_base:login') + '?next=' + self.url)

    def test_module_detail_view_get_login_not_headteacher(self):
        """
        If user is not headteacher, he is redirected to login page.
        """
        self.client.login(**test_credentials)
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse('auth_base:login') + '?next=' + self.url)

    def test_module_detail_view_get_login_headteacher(self):
        """
        If user is headteacher, module detail view is shown.
        """
        self.client.login(**headteacher_credentials)
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'study_base/module_detail.html')


class TaskDetailViewTests(TestCase):
    """
    Tests checking task detail view functionality.
    """

    def setUp(self):
        create_headteacher_user()
        create_test_user()

        task = create_test_task()

        self.url = reverse('study_base:task_detail', args=[task.id])

    def test_task_detail_view_get_no_login(self):
        """
        If user is not authenticated, he is redirected to login page.
        """
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse('auth_base:login') + '?next=' + self.url)

    def test_task_detail_view_get_login_not_headteacher(self):
        """
        If user is not headteacher, he is redirected to login page.
        """
        self.client.login(**test_credentials)
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse('auth_base:login') + '?next=' + self.url)

    def test_task_detail_view_get_login_headteacher(self):
        """
        If user is headteacher, task detail view is shown.
        """
        self.client.login(**headteacher_credentials)
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'study_base/task_detail.html')
