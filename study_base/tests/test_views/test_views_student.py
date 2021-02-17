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
This module containes tests checking study_base student views.
'''

from django.test import TestCase
from django.urls import reverse

from study_base.tests.utils import test_credentials, create_test_user, student_credentials, create_student_user


class StudentHomeViewTests(TestCase):
    """
    Tests checking student home view functionality.
    """

    def setUp(self):
        create_student_user()
        create_test_user()

        self.url = reverse('study_base:student_home')

    def test_student_home_view_get_no_login(self):
        """
        If user is not authenticated, he is redirected to login page.
        """
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse('auth_base:login') + '?next=' + self.url)

    def test_student_home_view_get_login_not_student(self):
        """
        If user is not student, he is redirected to login page.
        """
        self.client.login(**test_credentials)
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse('auth_base:login') + '?next=' + self.url)

    def test_student_home_view_get_login_student(self):
        """
        If user is student, student home view is shown.
        """
        self.client.login(**student_credentials)
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'study_base/student_home.html')
