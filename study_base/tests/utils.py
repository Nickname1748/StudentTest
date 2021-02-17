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

"""
This module contains often used functions and data for tests in main app.
"""

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.utils import timezone

from study_base.models import StudentGroup, TestModule, PlannedTest, PlannedTestModular, PlannedTestManual, TestTask


test_credentials = {
    'username': 'testuser',
    'password': 'testpass'
}


# admin_credentials = {
#     'username': 'admin',
#     'password': 'testpass'
# }


teacher_credentials = {
    'username': 'teacher',
    'password': 'testpass'
}


headteacher_credentials = {
    'username': 'headteacher',
    'password': 'testpass'
}


student_credentials = {
    'username': 'student1',
    'password': 'testpass'
}


def create_test_user():
    """
    Creates test user.
    """
    user = get_user_model().objects.create_user(
        **test_credentials,
        email='test@example.com',
        first_name='Name',
        last_name='Surname'
    )
    return user


# def create_admin_user():
#     """
#     Creates admin user.
#     """
#     admin = get_user_model().objects.create_user(
#         **admin_credentials,
#         email='admin@example.com',
#         first_name='AdminName',
#         last_name='AdminSurname'
#     )
#     admin.is_staff = True
#     admin.save()
#     return admin


def create_teacher_user():
    """
    Creates teacher user.
    """
    teacher = get_user_model().objects.create_user(
        **teacher_credentials,
        email='teacher@example.com',
        first_name='TeacherName',
        last_name='TeacherSurname'
    )
    group = Group.objects.get_or_create(name="Teacher")[0]
    teacher.groups.add(group)
    return teacher


def create_headteacher_user():
    """
    Creates headteacher user.
    """
    headteacher = get_user_model().objects.create_user(
        **headteacher_credentials,
        email='headteacher@example.com',
        first_name='HeadeacherName',
        last_name='HeadteacherSurname'
    )
    group = Group.objects.get_or_create(name="Headteacher")[0]
    headteacher.groups.add(group)
    return headteacher


def create_student_user():
    """
    Creates student user.
    """
    student = get_user_model().objects.create_user(
        **student_credentials,
        email='student@example.com',
        first_name='StudentName',
        last_name='StudentSurname'
    )
    group = Group.objects.get_or_create(name="Student")[0]
    student.groups.add(group)
    return student


def create_student_group(teacher=None):
    """
    Creates student group.
    """
    if not teacher:
        teacher = create_teacher_user()
    student_group = StudentGroup.objects.create(
        name="Group1",
        teacher=teacher
    )
    return student_group


def create_test_module():
    """
    Creates test module.
    """
    module = TestModule.objects.create(name="Module1")
    return module


def create_planned_test(student_group=None, teacher=None):
    """
    Creates planned test.
    """
    if not student_group:
        student_group = create_student_group(teacher=teacher)
    planned_test = PlannedTest.objects.create(
        name="Test1",
        student_group=student_group,
        begin_date=(timezone.now() - timezone.timedelta(days=1)),
        end_date=(timezone.now() + timezone.timedelta(days=1))
    )
    return planned_test


def create_test_modular(student_group=None, module=None, teacher=None):
    """
    Creates modular test.
    """
    if not student_group:
        student_group = create_student_group(teacher=teacher)
    if not module:
        module = create_test_module()
    test_modular = PlannedTestModular.objects.create(
        name="ModularTest1",
        student_group=student_group,
        begin_date=(timezone.now() - timezone.timedelta(days=1)),
        end_date=(timezone.now() + timezone.timedelta(days=1)),
        module=module,
        task_count=1
    )
    return test_modular


def create_test_manual(student_group=None, teacher=None):
    """
    Creates manual test.
    """
    if not student_group:
        student_group = create_student_group(teacher=teacher)
    planned_test = PlannedTestManual.objects.create(
        name="ManualTest1",
        student_group=student_group,
        begin_date=(timezone.now() - timezone.timedelta(days=1)),
        end_date=(timezone.now() + timezone.timedelta(days=1))
    )
    return planned_test


def create_test_task(module=None):
    """
    Creates empty task.
    """
    if not module:
        module = create_test_module()
    task = TestTask.objects.create(
        task_description="Task1",
        module=module
    )
    return task
