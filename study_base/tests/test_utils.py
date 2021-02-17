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
This module containes tests checking study_base utils functions.
'''

from django.test import TestCase

from study_base.utils import assert_test_task_single_choice, assert_test_task_multiple_choice, assert_test_task_text
from .utils import create_test_task_single_choice, create_test_task_multiple_choice, create_test_task_text


class AssertTestTaskSingleChoiceTests(TestCase):
    """
    Tests checking assert_test_task_single_choice() function.
    """

    def setUp(self):
        self.task = create_test_task_single_choice()

    def test_assert_test_task_single_choice_answer_none(self):
        """
        Should return False if None is passed.
        """
        self.assertFalse(assert_test_task_single_choice(answer=None))

    def test_assert_test_task_single_choice_answer_wrong_1(self):
        """
        Should return False if wrong answer is passed.
        """
        item1 = self.task.testtasksinglechoiceitem_set.filter(text="1")[0].id
        self.assertFalse(assert_test_task_single_choice(answer=item1))

    def test_assert_test_task_single_choice_answer_right_2(self):
        """
        Should return True if right answer is passed.
        """
        item2 = self.task.testtasksinglechoiceitem_set.filter(text="2")[0].id
        self.assertTrue(assert_test_task_single_choice(answer=item2))

    def test_assert_test_task_single_choice_answer_wrong_3(self):
        """
        Should return False if wrong answer is passed.
        """
        item3 = self.task.testtasksinglechoiceitem_set.filter(text="3")[0].id
        self.assertFalse(assert_test_task_single_choice(answer=item3))


class AssertTestTaskMultipleChoiceTests(TestCase):
    """
    Tests checking assert_test_task_multiple_choice() function.
    """

    def setUp(self):
        self.task = create_test_task_multiple_choice()
        self.item1 = str(self.task.testtaskmultiplechoiceitem_set.filter(text="1")[0].id)
        self.item2 = str(self.task.testtaskmultiplechoiceitem_set.filter(text="2")[0].id)
        self.item3 = str(self.task.testtaskmultiplechoiceitem_set.filter(text="3")[0].id)

    def test_assert_test_task_multiple_choice_answer_none(self):
        """
        Should return False if None is passed.
        """
        self.assertFalse(assert_test_task_multiple_choice(task=self.task, answer=None))

    def test_assert_test_task_single_choice_answer_wrong_empty(self):
        """
        Should return False if wrong answer is passed.
        """
        self.assertFalse(assert_test_task_multiple_choice(task=self.task, answer='[]'))

    def test_assert_test_task_single_choice_answer_wrong_1(self):
        """
        Should return False if wrong answer is passed.
        """
        answer = [self.item1]
        self.assertFalse(assert_test_task_multiple_choice(task=self.task, answer=str(answer)))

    def test_assert_test_task_single_choice_answer_wrong_2(self):
        """
        Should return False if wrong answer is passed.
        """
        answer = [self.item2]
        self.assertFalse(assert_test_task_multiple_choice(task=self.task, answer=str(answer)))

    def test_assert_test_task_single_choice_answer_wrong_3(self):
        """
        Should return False if wrong answer is passed.
        """
        answer = [self.item3]
        self.assertFalse(assert_test_task_multiple_choice(task=self.task, answer=str(answer)))

    def test_assert_test_task_single_choice_answer_wrong_1_2(self):
        """
        Should return False if wrong answer is passed.
        """
        answer = [self.item1, self.item2]
        self.assertFalse(assert_test_task_multiple_choice(task=self.task, answer=str(answer)))

    def test_assert_test_task_single_choice_answer_wrong_1_3(self):
        """
        Should return False if wrong answer is passed.
        """
        answer = [self.item1, self.item3]
        self.assertFalse(assert_test_task_multiple_choice(task=self.task, answer=str(answer)))

    def test_assert_test_task_single_choice_answer_right_2_3(self):
        """
        Should return True if right answer is passed.
        """
        answer = [self.item2, self.item3]
        self.assertTrue(assert_test_task_multiple_choice(task=self.task, answer=str(answer)))

    def test_assert_test_task_single_choice_answer_wrong_1_2_3(self):
        """
        Should return False if wrong answer is passed.
        """
        answer = [self.item1, self.item2, self.item3]
        self.assertFalse(assert_test_task_multiple_choice(task=self.task, answer=str(answer)))


class AssertTestTaskTextTests(TestCase):
    """
    Tests checking assert_test_task_text() function.
    """

    def setUp(self):
        self.task = create_test_task_text()

    def test_assert_test_task_single_choice_answer_none(self):
        """
        Should return False if None is passed.
        """
        self.assertFalse(assert_test_task_text(task=self.task, answer=None))

    def test_assert_test_task_single_choice_answer_right(self):
        """
        Should return True if right answer is passed.
        """
        self.assertTrue(assert_test_task_text(task=self.task, answer="Answer1"))

    def test_assert_test_task_single_choice_answer_wrong(self):
        """
        Should return False if wrong answer is passed.
        """
        self.assertFalse(assert_test_task_text(task=self.task, answer="Answer2"))
