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
This module contains study forms.
"""

from django import forms

from .models import PlannedTestManual, PlannedTestModular, TestModule, TestTaskMultipleChoice, TestTaskMultipleChoiceItem, TestTaskSingleChoice, TestTaskSingleChoiceItem, TestTaskText


class PlanTestModularForm(forms.ModelForm):
    """
    Form for planning a modular test.
    """
    class Meta:
        model = PlannedTestModular
        fields = ['name', 'student_group', 'begin_date', 'end_date', 'module', 'task_count']


class PlanTestManualForm(forms.ModelForm):
    """
    Form for planning a manual test.
    """
    class Meta:
        model = PlannedTestManual
        fields = ['name', 'student_group', 'begin_date', 'end_date', 'tasks']


class CreateTestModuleForm(forms.ModelForm):
    """
    Form for creating test modules.
    """
    class Meta:
        model = TestModule
        fields = ['name']


class CreateTestTaskSingleChoiceItemForm(forms.ModelForm):
    """
    Form for creating test single choice task item.
    """
    class Meta:
        model = TestTaskSingleChoiceItem
        fields = ['text', 'is_right']


class CreateTestTaskMultipleChoiceItemForm(forms.ModelForm):
    """
    Form for creating test multiple choice task item.
    """
    class Meta:
        model = TestTaskMultipleChoiceItem
        fields = ['text', 'is_right']


CreateTestTaskSingleChoiceItemFormSet = forms.formset_factory(CreateTestTaskSingleChoiceItemForm)


CreateTestTaskMultipleChoiceItemFormSet = forms.formset_factory(CreateTestTaskMultipleChoiceItemForm)


class CreateTestTaskSingleChoiceForm(forms.ModelForm):
    """
    Form for creating test single choice task.
    """
    class Meta:
        model = TestTaskSingleChoice
        fields = ['task_description', 'module']


class CreateTestTaskMultipleChoiceForm(forms.ModelForm):
    """
    Form for creating test multiple choice task.
    """
    class Meta:
        model = TestTaskMultipleChoice
        fields = ['task_description', 'module']


class CreateTestTaskTextForm(forms.ModelForm):
    """
    Form for creating test text task.
    """
    class Meta:
        model = TestTaskText
        fields = ['task_description', 'module', 'answer']


class TakeTestTaskSingleChoiceForm(forms.Form):
    """
    Form for taking test single choice task.
    """
    answer = forms.ChoiceField(widget=forms.RadioSelect())

    def __init__(self, *args, **kwargs):
        choices = kwargs.pop('choices', ())
        super().__init__(*args, **kwargs)
        self.fields['answer'].choices = choices


class TakeTestTaskMultipleChoiceForm(forms.Form):
    """
    Form for taking test multiple choice task.
    """
    answer = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple())

    def __init__(self, *args, **kwargs):
        choices = kwargs.pop('choices', ())
        super().__init__(*args, **kwargs)
        self.fields['answer'].choices = choices


class TakeTestTaskTextForm(forms.Form):
    """
    Form for taking test text task.
    """
    answer = forms.CharField(max_length=255)
