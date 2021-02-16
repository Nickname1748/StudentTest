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
This module containes tests checking study_base common views.
'''

from django.test import TestCase
from django.urls import reverse

from study_base.tests.utils import headteacher_credentials, create_headteacher_user, teacher_credentials, create_teacher_user, student_credentials, create_student_user, test_credentials, create_test_user


class IndexViewTests(TestCase):
    """
    Tests checking index view functionality.
    """

    def setUp(self):
        create_headteacher_user()
        create_teacher_user()
        create_student_user()
        create_test_user()

        self.url = reverse('study_base:index')

    def test_index_view_get_no_login(self):
        """
        If user is not authenticated, he is redirected to login page.
        """
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse('auth_base:login') + '?next=' + self.url)

    def test_index_view_get_login_headteacher(self):
        """
        If user is headteacher, he is redirected to headteacher page.
        """
        self.client.login(**headteacher_credentials)
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse('study_base:headteacher_home'))

    def test_index_view_get_login_teacher(self):
        """
        If user is teacher, he is redirected to teacher page.
        """
        self.client.login(**teacher_credentials)
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse('study_base:teacher_home'))

    def test_index_view_get_login_student(self):
        """
        If user is student, he is redirected to student page.
        """
        self.client.login(**student_credentials)
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse('study_base:student_home'))

    def test_index_view_get_login_unknown(self):
        """
        If unknown is other, error 404 is returned.
        """
        self.client.login(**test_credentials)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 404)
