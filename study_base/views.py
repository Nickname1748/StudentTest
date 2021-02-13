"""
This module contains test views.
"""

import random
import ast

from django.http.response import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.utils.decorators import method_decorator
from django.utils import timezone

from .models import PlannedTestModular, StudentGroup, PlannedTest, TestAttempt, TestModule, TestTaskMultipleChoiceItem, TestTaskSingleChoice, TestTaskSingleChoiceItem, TestTaskMultipleChoice
from .decorators import group_required
from .forms import (
    CreateTestTaskMultipleChoiceForm, CreateTestTaskMultipleChoiceItemFormSet, PlanTestModularForm, CreateTestModuleForm, CreateTestTaskSingleChoiceForm,
    CreateTestTaskSingleChoiceItemFormSet, TakeTestTaskSingleChoiceForm, TakeTestTaskMultipleChoiceForm)


@method_decorator(group_required("Teacher"), name='dispatch')
class TeacherHomeView(TemplateView):
    """
    Teacher home view.
    """
    template_name = 'study_base/teacher_home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['studentgroup_list'] = self.request.user.group_teacher.all()
        context['plannedtest_list'] = PlannedTest.objects.filter(
            student_group__teacher__username__exact=self.request.user.username).filter(end_date__gt=timezone.now())
        return context


@method_decorator(group_required("Teacher"), name='dispatch')
class PlanTestModularView(CreateView):
    """
    Planning modular test view.
    """
    model = PlannedTestModular
    template_name = 'study_base/plan_test.html'
    form_class = PlanTestModularForm
    success_url = reverse_lazy('study_base:teacher_home')


@method_decorator(group_required("Teacher"), name='dispatch')
class EditTestModularView(UpdateView):
    """
    Updating modular test view.
    """
    model = PlannedTestModular
    template_name = 'study_base/plan_test.html'
    form_class = PlanTestModularForm
    success_url = reverse_lazy('study_base:teacher_home')


@method_decorator(group_required("Teacher"), name='dispatch')
class CreateTestModuleView(CreateView):
    """
    Creating test module view.
    """
    model = TestModule
    template_name = 'study_base/create_module.html'
    form_class = CreateTestModuleForm
    success_url = reverse_lazy('study_base:teacher_home')


@method_decorator(group_required("Teacher"), name='dispatch')
class EditTestModuleView(UpdateView):
    """
    Update test module view.
    """
    model = TestModule
    template_name = 'study_base/create_module.html'
    form_class = CreateTestModuleForm
    success_url = reverse_lazy('study_base:teacher_home')


@method_decorator(group_required("Teacher"), name='dispatch')
class CreateTestTaskSingleChoiceView(CreateView):
    """
    Creating single choice test task view.
    """
    template_name = 'study_base/create_task.html'
    form_class = CreateTestTaskSingleChoiceForm
    success_url = reverse_lazy('study_base:teacher_home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = CreateTestTaskSingleChoiceItemFormSet(self.request.POST)
        else:
            context['formset'] = CreateTestTaskSingleChoiceItemFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        if formset.is_valid():
            self.object = form.save()
            for cleaned_data in formset.cleaned_data:
                if len(cleaned_data) > 0:
                    item = TestTaskSingleChoiceItem(task=self.object, **cleaned_data)
                    item.save()
            return super().form_valid(form)
        else:
            return self.form_invalid(form)


@method_decorator(group_required("Teacher"), name='dispatch')
class CreateTestTaskMultipleChoiceView(CreateView):
    """
    Creating multiple choice test task view.
    """
    template_name = 'study_base/create_task.html'
    form_class = CreateTestTaskMultipleChoiceForm
    success_url = reverse_lazy('study_base:teacher_home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = CreateTestTaskMultipleChoiceItemFormSet(self.request.POST)
        else:
            context['formset'] = CreateTestTaskMultipleChoiceItemFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        if formset.is_valid():
            self.object = form.save()
            for cleaned_data in formset.cleaned_data:
                if len(cleaned_data) > 0:
                    item = TestTaskMultipleChoiceItem(task=self.object, **cleaned_data)
                    item.save()
            return super().form_valid(form)
        else:
            return self.form_invalid(form)


@method_decorator(group_required("Student"), name='dispatch')
class StudentHomeView(TemplateView):
    """
    Student home view.
    """
    template_name = 'study_base/student_home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['studentgroup_list'] = self.request.user.group_students.all()
        context['plannedtest_list'] = PlannedTest.objects.filter(
            student_group__in=context['studentgroup_list']).filter(end_date__gt=timezone.now())
        return context


@group_required("Student")
def take_test(request, test_id):
    """
    Take test view.
    """
    test = get_object_or_404(PlannedTest, pk=test_id)
    if test.student_group not in request.user.group_students.all():
        return redirect('study_base:student_home')
    if not test.is_active():
        return redirect('study_base:student_home')
    if request.user.testattempt_set.filter(test__id=test_id).filter(finish_date__isnull=True).exists():
        attempt = request.user.testattempt_set.filter(test__id=test_id).filter(finish_date__isnull=True)[0]
        return redirect('study_base:take_test_task', attempt.id, 0)
    if PlannedTestModular.objects.filter(pk=test_id).exists():
        return take_test_modular(request, test_id)
    return redirect('study_base:student_home')


def take_test_modular(request, test_id):
    """
    Take modular test view.
    """
    test = get_object_or_404(PlannedTestModular, pk=test_id)
    # Generate variant
    tasks = random.sample(list(test.module.testtask_set.all()), test.task_count)
    attempt = TestAttempt(student=request.user, test=test)
    attempt.save()
    attempt.tasks.set(tasks)
    attempt.save()
    return redirect('study_base:take_test_task', attempt.id, 0)


@group_required("Student")
def take_test_task(request, attempt_id, task_num):
    """
    Test task view.
    """
    attempt = get_object_or_404(TestAttempt, pk=attempt_id)
    if task_num >= attempt.tasks.count():
        raise Http404("Wrong task number")
    task = attempt.tasks.all()[task_num]
    if TestTaskSingleChoice.objects.filter(id=task.id).exists():
        return take_test_task_single_choice(request, attempt, task, task_num)
    if TestTaskMultipleChoice.objects.filter(id=task.id).exists():
        return take_test_task_multiple_choice(request, attempt, task, task_num)
    return redirect('study_base:student_home')


def take_test_task_single_choice(request, attempt, task, task_num):
    """
    Test task single choice view.
    """
    items = task.testtasksinglechoice.testtasksinglechoiceitem_set.all()
    choices = [(item.id, item.text) for item in items]
    if request.method == 'POST':
        form = TakeTestTaskSingleChoiceForm(request.POST, choices=choices)
        if form.is_valid():
            answer = form.cleaned_data['answer']
            attempt_task = task.testattempttask_set.filter(attempt=attempt)[0]
            attempt_task.answer = answer
            attempt_task.save()
        if task_num+1 >= attempt.tasks.count():
            return end_test_attempt(request, attempt)
        else:
            return redirect('study_base:take_test_task', attempt.id, task_num+1)
    else:
        form = TakeTestTaskSingleChoiceForm(choices=choices)
        context = {'form': form, 'text': task.task_description}
        return render(request, 'study_base/take_test.html', context)


def take_test_task_multiple_choice(request, attempt, task, task_num):
    """
    Test task multiple choice view.
    """
    items = task.testtaskmultiplechoice.testtaskmultiplechoiceitem_set.all()
    choices = [(item.id, item.text) for item in items]
    if request.method == 'POST':
        form = TakeTestTaskMultipleChoiceForm(request.POST, choices=choices)
        if form.is_valid():
            answer = form.cleaned_data['answer']
            attempt_task = task.testattempttask_set.filter(attempt=attempt)[0]
            attempt_task.answer = answer
            attempt_task.save()
        if task_num+1 >= attempt.tasks.count():
            return end_test_attempt(request, attempt)
        else:
            return redirect('study_base:take_test_task', attempt.id, task_num+1)
    else:
        form = TakeTestTaskMultipleChoiceForm(choices=choices)
        context = {'form': form, 'text': task.task_description}
        return render(request, 'study_base/take_test.html', context)


def end_test_attempt(request, attempt):
    """
    Ends test attempt.
    """
    attempt.finish_date = timezone.now()
    # Calculate result
    right = 0
    total = attempt.tasks.count()
    for attempt_task in attempt.testattempttask_set.all():
        task = attempt_task.task
        if TestTaskSingleChoice.objects.filter(id=task.id).exists():
            if assert_test_task_single_choice(attempt_task.answer):
                right += 1
        if TestTaskMultipleChoice.objects.filter(id=task.id).exists():
            if assert_test_task_multiple_choice(attempt_task.task, attempt_task.answer):
                right += 1
    result = right / total
    attempt.result = result
    attempt.save()
    return redirect('study_base:attempt_results', attempt.id)


def assert_test_task_single_choice(answer):
    """
    Checks if answer is right in single choice task
    """
    chosen_item = TestTaskSingleChoiceItem.objects.get(pk=answer)
    return chosen_item.is_right


def assert_test_task_multiple_choice(task, answer):
    """
    Checks if answer is right in multiple choice task
    """
    answer = ast.literal_eval(answer)
    items = task.testtaskmultiplechoice.testtaskmultiplechoiceitem_set.all()
    for item in items:
        if item.is_right and str(item.id) not in answer:
            return False
        if not item.is_right and str(item.id) in answer:
            return False
    return True


@method_decorator(group_required("Student"), name='dispatch')
class TestAttemptResultsView(DetailView):
    """
    Show test attempt results.
    """
    model = TestAttempt
    template_name = 'study_base/attempt_results.html'
