"""
This module contains study forms.
"""

from django import forms

from .models import PlannedTestModular, TestModule, TestTaskSingleChoice, TestTaskSingleChoiceItem


class PlanTestModularForm(forms.ModelForm):
    """
    Form for planning a modular test.
    """
    class Meta:
        model = PlannedTestModular
        fields = ['student_group', 'begin_date', 'end_date', 'module', 'task_count']


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


CreateTestTaskSingleChoiceItemFormSet = forms.formset_factory(CreateTestTaskSingleChoiceItemForm)


class CreateTestTaskSingleChoiceForm(forms.ModelForm):
    """
    Form for creating test single choice task.
    """
    class Meta:
        model = TestTaskSingleChoice
        fields = ['task_description', 'module']
