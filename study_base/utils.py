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
This module contains additional study and test functions.
"""

import ast

from .models import TestTaskSingleChoiceItem


def assert_test_task_single_choice(answer):
    """
    Checks if answer is right in single choice task
    """
    if not answer:
        return False
    chosen_item = TestTaskSingleChoiceItem.objects.get(pk=answer)
    return chosen_item.is_right


def assert_test_task_multiple_choice(task, answer):
    """
    Checks if answer is right in multiple choice task
    """
    if not answer:
        return False
    answer = ast.literal_eval(answer)
    items = task.testtaskmultiplechoice.testtaskmultiplechoiceitem_set.all()
    for item in items:
        if item.is_right and str(item.id) not in answer:
            return False
        if not item.is_right and str(item.id) in answer:
            return False
    return True


def assert_test_task_text(task, answer):
    """
    Checks if answer is right in text task
    """
    return task.testtasktext.answer == answer
