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
This module containes tests checking study_base teacher views.
'''

from django.test import TestCase
from django.urls import reverse

from study_base.tests.utils import create_student_group, create_test_manual, create_test_modular, teacher_credentials, create_teacher_user, test_credentials, create_test_user, create_planned_test


class TeacherHomeViewTests(TestCase):
    """
    Tests checking teacher home view functionality.
    """

    def setUp(self):
        create_teacher_user()
        create_test_user()

        self.url = reverse('study_base:teacher_home')

    def test_index_view_get_no_login(self):
        """
        If user is not authenticated, he is redirected to login page.
        """
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse('auth_base:login') + '?next=' + self.url)

    def test_index_view_get_login_not_teacher(self):
        """
        If user is not teacher, he is redirected to login page.
        """
        self.client.login(**test_credentials)
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse('auth_base:login') + '?next=' + self.url)

    def test_index_view_get_login_teacher(self):
        """
        If user is teacher, he is redirected to teacher page.
        """
        self.client.login(**teacher_credentials)
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'study_base/teacher_home.html')


class EditTestViewTests(TestCase):
    """
    Tests checking edit test view functionality.
    """

    def setUp(self):
        teacher = create_teacher_user()
        create_test_user()

        student_group = create_student_group(teacher=teacher)

        test_empty = create_planned_test(student_group=student_group)
        self.empty_id = test_empty.id

        test_modular = create_test_modular(student_group=student_group)
        self.modular_id = test_modular.id

        test_manual = create_test_manual(student_group=student_group)
        self.manual_id = test_manual.id

    def test_edit_test_view_get_no_login(self):
        """
        If user is not authenticated, he is redirected to login page.
        """
        url = reverse('study_base:edit_test', args=[self.empty_id])
        response = self.client.get(url)
        self.assertRedirects(response, reverse('auth_base:login') + '?next=' + url)

    def test_edit_test_view_get_login_not_teacher(self):
        """
        If user is not teacher, he is redirected to login page.
        """
        url = reverse('study_base:edit_test', args=[self.empty_id])
        self.client.login(**test_credentials)
        response = self.client.get(url)
        self.assertRedirects(response, reverse('auth_base:login') + '?next=' + url)

    def test_edit_test_view_get_login_teacher_empty(self):
        """
        If test is nonexistent, error 404 is returned.
        """
        url = reverse('study_base:edit_test', args=[self.empty_id])
        self.client.login(**teacher_credentials)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_edit_test_view_get_login_teacher_modular(self):
        """
        If test is modular, user is redirected to edit modular test view.
        """
        url = reverse('study_base:edit_test', args=[self.modular_id])
        self.client.login(**teacher_credentials)
        response = self.client.get(url)
        self.assertRedirects(response, reverse('study_base:edit_test_modular', args=[self.modular_id]))

    def test_edit_test_view_get_login_teacher_manual(self):
        """
        If test is manual, user is redirected to edit manual test view.
        """
        url = reverse('study_base:edit_test', args=[self.manual_id])
        self.client.login(**teacher_credentials)
        response = self.client.get(url)
        self.assertRedirects(response, reverse('study_base:edit_test_manual', args=[self.manual_id]))
