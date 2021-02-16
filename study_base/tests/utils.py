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

from study_base.models import StudentGroup, PlannedTest


admin_credentials = {
    'username': 'admin',
    'password': 'testpass'
}


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


# def create_test_user():
#     """
#     Creates test user.
#     """
#     user = get_user_model().objects.create_user(
#         **test_credentials,
#         email='test@example.com',
#         first_name='Name',
#         last_name='Surname'
#     )
#     return user


def create_admin_user():
    """
    Creates admin user.
    """
    admin = get_user_model().objects.create_user(
        **admin_credentials,
        email='admin@example.com',
        first_name='AdminName',
        last_name='AdminSurname'
    )
    admin.is_staff = True
    admin.save()
    return admin


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


def create_student_group():
    """
    Creates student group.
    """
    teacher = create_teacher_user()
    student_group = StudentGroup.objects.create(
        name="Group1",
        teacher=teacher
    )
    return student_group


def create_planned_test():
    """
    Creates planned test.
    """
    student_group = create_student_group()
    planned_test = PlannedTest.objects.create(
        name="Test1",
        student_group=student_group,
        begin_date=(timezone.now() - timezone.timedelta(days=1)),
        end_date=(timezone.now() + timezone.timedelta(days=1))
    )
    return planned_test
