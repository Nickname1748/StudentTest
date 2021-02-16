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
This module containes tests checking study_base models
'''

from django.test import TestCase
from django.utils import timezone

from study_base.models import TestAttempt, TestModule, TestTask

from .utils import create_student_user, create_test_module, create_student_group, create_planned_test


class StudentGroupModelTests(TestCase):
    """
    Tests checking student group model.
    """

    def setUp(self):
        self.student_group = create_student_group()

    def test_student_group_str(self):
        """
        __str__() should return student group name.
        """
        self.assertEqual(str(self.student_group), "Group1")


class TestModuleModelTests(TestCase):
    """
    Tests checking test module model.
    """

    def setUp(self):
        self.module = create_test_module()

    def test_module_str(self):
        """
        __str__() should return test module name.
        """
        self.assertEqual(str(self.module), "Module1")


class TestTaskModelTests(TestCase):
    """
    Tests checking test task model.
    """

    def setUp(self):
        module = create_test_module()
        self.task = TestTask.objects.create(
            task_description="Task1",
            module=module
        )

    def test_task_str(self):
        """
        __str__() should return test task description.
        """
        self.assertEqual(str(self.task), "Task1")


class PlannedTestModelTests(TestCase):
    """
    Tests checking planned test model.
    """

    def setUp(self):
        self.planned_test = create_planned_test()

    def test_planned_test_str(self):
        """
        __str__() should return test task description.
        """
        self.assertEqual(str(self.planned_test), "Test1")

    def test_planned_test_is_active_active(self):
        """
        If test is active, is_active() returns True.
        """
        self.assertTrue(self.planned_test.is_active())

    def test_planned_test_is_active_inactive(self):
        """
        If test is inactive, is_active() returns False.
        """
        self.planned_test.begin_date = (timezone.now() + timezone.timedelta(hours=1))
        self.assertFalse(self.planned_test.is_active())

    def test_planned_test_is_active_expired(self):
        """
        If test is expired, is_active() returns False.
        """
        self.planned_test.end_date = (timezone.now() - timezone.timedelta(hours=1))
        self.assertFalse(self.planned_test.is_active())


class TestAttemptModelTests(TestCase):
    """
    Tests checking test attempt model.
    """

    def setUp(self):
        planned_test = create_planned_test()
        student = create_student_user()
        self.test_attempt = TestAttempt.objects.create(
            student=student,
            test=planned_test
        )

    def test_attempt_is_finished_not_finished(self):
        """
        If test attempt is not finished, is_finished() returns False.
        """
        self.assertFalse(self.test_attempt.is_finished())

    def test_attempt_is_finished_finished(self):
        """
        If test attempt is finished, is_finished() returns True.
        """
        self.test_attempt.finish_date = timezone.now()
        self.assertTrue(self.test_attempt.is_finished())

    def test_attempt_result_percent_zero(self):
        """
        If test attempt result percent is 0, result_percent() returns "0.0%".
        """
        self.test_attempt.finish_date = timezone.now()
        self.test_attempt.result = 0
        self.assertEqual(self.test_attempt.result_percent(), "0.0%")

    def test_attempt_result_percent_full(self):
        """
        If test attempt result percent is 1, result_percent() returns "100.0%".
        """
        self.test_attempt.finish_date = timezone.now()
        self.test_attempt.result = 1
        self.assertEqual(self.test_attempt.result_percent(), "100.0%")

    def test_attempt_result_percent_third(self):
        """
        If test attempt result percent is 1/3, result_percent() returns "33.3%".
        """
        self.test_attempt.finish_date = timezone.now()
        self.test_attempt.result = 1/3
        self.assertEqual(self.test_attempt.result_percent(), "33.3%")

    def test_attempt_result_percent_two_thirds(self):
        """
        If test attempt result percent is 2/3, result_percent() returns "66.7%".
        """
        self.test_attempt.finish_date = timezone.now()
        self.test_attempt.result = 2/3
        self.assertEqual(self.test_attempt.result_percent(), "66.7%")
