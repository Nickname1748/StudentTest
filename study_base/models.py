"""
This module contains essential study and test modules
"""

import uuid

from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy


class StudentGroup(models.Model):
    """
    Group of students to test
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name=gettext_lazy('ID')
    )
    name = models.CharField(max_length=255, verbose_name=gettext_lazy('Name'))
    teacher = models.ForeignKey(
        get_user_model(),
        on_delete=models.PROTECT,
        verbose_name=gettext_lazy('Teacher'),
        related_name='group_teacher'
    )
    students = models.ManyToManyField(get_user_model(), related_name='group_students')

    def __str__(self):
        return self.name


class TestModule(models.Model):
    """
    Module of similar tasks.
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name=gettext_lazy('ID')
    )
    name = models.CharField(max_length=255, verbose_name=gettext_lazy('Name'))

    def __str__(self):
        return self.name


class TestTask(models.Model):
    """
    Abstract model for test task.
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name=gettext_lazy('ID')
    )
    task_description = models.TextField(verbose_name=gettext_lazy('Task description'))
    module = models.ForeignKey(
        TestModule,
        on_delete=models.CASCADE,
        verbose_name=gettext_lazy('Module')
    )


class TestTaskSingleChoice(TestTask):
    """
    Simple task with single choice.
    """


class TestTaskMultipleChoice(TestTask):
    """
    Simple task with multiple choice.
    """


class TestTaskChoiceItem(models.Model):
    """
    Abstract model for choice item.
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name=gettext_lazy('ID')
    )
    text = models.CharField(max_length=255, verbose_name=gettext_lazy('Text'))
    is_right = models.BooleanField(verbose_name=gettext_lazy('Right'))



class TestTaskSingleChoiceItem(TestTaskChoiceItem):
    """
    Single choice item.
    """
    task = models.ForeignKey(
        TestTaskSingleChoice,
        on_delete=models.CASCADE,
        verbose_name=gettext_lazy('Task')
    )


class TestTaskMultipleChoiceItem(TestTaskChoiceItem):
    """
    Multiple choice item.
    """
    task = models.ForeignKey(
        TestTaskMultipleChoice,
        on_delete=models.CASCADE,
        verbose_name=gettext_lazy('Task')
    )


class TestTaskText(TestTask):
    """
    Task with text answer.
    """
    answer = models.CharField(max_length=255, verbose_name=gettext_lazy('Answer'))


class PlannedTest(models.Model):
    """
    A planned test abstract model.
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name=gettext_lazy('ID')
    )
    student_group = models.ForeignKey(
        StudentGroup,
        on_delete=models.PROTECT,
        verbose_name=gettext_lazy('Student group')
    )
    begin_date = models.DateTimeField(verbose_name=gettext_lazy('Begin date'))
    end_date = models.DateTimeField(verbose_name=gettext_lazy('End date'))


class PlannedTestModular(PlannedTest):
    """
    Test with random tasks based on modules.
    """
    module = models.ForeignKey(
        TestModule,
        on_delete=models.PROTECT,
        verbose_name=gettext_lazy('Module')
    )
    task_count = models.PositiveSmallIntegerField(verbose_name=gettext_lazy('Task count'))


class PlannedTestManual(PlannedTest):
    """
    Test with manually selected tasks.
    """
    tasks = models.ManyToManyField(TestTask, verbose_name=gettext_lazy('Tasks'))


class TestAttempt(models.Model):
    """
    Test attempt abstract model.
    """
    start_date = models.DateTimeField(auto_now_add=True, verbose_name=gettext_lazy('Start date'))
    finish_date = models.DateTimeField(null=True, verbose_name=gettext_lazy('Finish date'))


class TestAttemptModular(TestAttempt):
    """
    Modular test attempt model.
    """
    test = models.ForeignKey(
        PlannedTestModular,
        on_delete=models.PROTECT,
        verbose_name=gettext_lazy('Test')
    )


class TestAttemptManual(TestAttempt):
    """
    Manually selected test attempt model.
    """
    test = models.ForeignKey(
        PlannedTestManual,
        on_delete=models.PROTECT,
        verbose_name=gettext_lazy('Test')
    )
