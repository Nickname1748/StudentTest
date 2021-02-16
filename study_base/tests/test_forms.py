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
This module containes tests checking study_base forms
'''

from django.test import TestCase

from study_base.forms import TakeTestTaskSingleChoiceForm, TakeTestTaskMultipleChoiceForm


class TakeTestTaskSingleChoiceFormTests(TestCase):
    """
    Tests checking single choice form.
    """

    def test_take_test_task_single_choice_form_init(self):
        """
        Form should initialize with choices passed into initializer.
        """
        choices = [
            ('d9840c39-b66a-44ba-8e5d-8e2a0b6a1221', 'Choice1'),
            ('dfca8810-c24a-4127-8791-f734f89d8fb0', 'Choice2'),
            ('23de15e6-ac38-421c-b197-f7788d58ba1c', 'Choice3'),
            ('ff13466b-b713-4b8e-b6e3-a265ad22fe52', 'Choice4'),
        ]
        form = TakeTestTaskSingleChoiceForm(choices=choices)
        self.assertEqual(form.fields['answer'].choices, choices)


class TakeTestTaskMultipleChoiceFormTests(TestCase):
    """
    Tests checking multiple choice form.
    """

    def test_take_test_task_multiple_choice_form_init(self):
        """
        Form should initialize with choices passed into initializer.
        """
        choices = [
            ('d9840c39-b66a-44ba-8e5d-8e2a0b6a1221', 'Choice1'),
            ('dfca8810-c24a-4127-8791-f734f89d8fb0', 'Choice2'),
            ('23de15e6-ac38-421c-b197-f7788d58ba1c', 'Choice3'),
            ('ff13466b-b713-4b8e-b6e3-a265ad22fe52', 'Choice4'),
        ]
        form = TakeTestTaskMultipleChoiceForm(choices=choices)
        self.assertEqual(form.fields['answer'].choices, choices)
