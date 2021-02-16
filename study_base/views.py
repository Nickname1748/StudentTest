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
This module contains test views.
"""

import random
import ast
from django.contrib.auth.models import Group

from django.http.response import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.utils.decorators import method_decorator
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext as _

from .models import PlannedTestManual, PlannedTestModular, StudentGroup, PlannedTest, TestAttempt, TestModule, TestTask, TestTaskMultipleChoiceItem, TestTaskSingleChoice, TestTaskSingleChoiceItem, TestTaskMultipleChoice, TestTaskText
from .decorators import group_required
from .forms import (
    CreateTestTaskMultipleChoiceForm, CreateTestTaskMultipleChoiceItemFormSet, CreateTestTaskTextForm, PlanTestManualForm, PlanTestModularForm, CreateTestModuleForm, CreateTestTaskSingleChoiceForm,
    CreateTestTaskSingleChoiceItemFormSet, TakeTestTaskSingleChoiceForm, TakeTestTaskMultipleChoiceForm, TakeTestTaskTextForm)


@login_required
def index_view(request):
    """
    Index view for study.
    """
    if request.user.groups.filter(name="Headteacher").exists():
        return redirect('study_base:headteacher_home')
    if request.user.groups.filter(name="Teacher").exists():
        return redirect('study_base:teacher_home')
    if request.user.groups.filter(name="Student").exists():
        return redirect('study_base:student_home')
    raise Http404('User is not active yet.')


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
class PlanTestManualView(CreateView):
    """
    Planning manual test view.
    """
    model = PlannedTestManual
    template_name = 'study_base/plan_test.html'
    form_class = PlanTestManualForm
    success_url = reverse_lazy('study_base:teacher_home')


@method_decorator(group_required("Teacher"), name='dispatch')
class EditTestManualView(UpdateView):
    """
    Updating manual test view.
    """
    model = PlannedTestManual
    template_name = 'study_base/plan_test.html'
    form_class = PlanTestManualForm
    success_url = reverse_lazy('study_base:teacher_home')


@group_required("Teacher")
def edit_test(request, test_id):
    """
    Updating test view.
    """
    if PlannedTestModular.objects.filter(pk=test_id).exists():
        return redirect('study_base:edit_test_modular', test_id)
    if PlannedTestManual.objects.filter(pk=test_id).exists():
        return redirect('study_base:edit_test_manual', test_id)
    raise Http404(_('No such test exist'))


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
            context['form_type'] = "single"
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
            context['form_type'] = "multiple"
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


@method_decorator(group_required("Teacher"), name='dispatch')
class CreateTestTaskTextView(CreateView):
    """
    Creating text test task view.
    """
    template_name = 'study_base/create_task.html'
    form_class = CreateTestTaskTextForm
    success_url = reverse_lazy('study_base:teacher_home')


@method_decorator(group_required("Teacher", "Headteacher"), name='dispatch')
class PlannedTestDetailView(DetailView):
    """
    View showing test results.
    """
    model = PlannedTest
    template_name = 'study_base/planned_test_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        planned_test = self.get_object()
        group = planned_test.student_group
        results = []
        for student in group.students.all():
            results.append((student, planned_test.testattempt_set.filter(student=student)))
        context['results'] = results
        return context


@method_decorator(group_required("Teacher"), name='dispatch')
class GroupDetailView(DetailView):
    """
    Group detail view.
    """
    model = StudentGroup
    template_name = 'study_base/group_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tests'] = self.get_object().plannedtest_set.all()
        return context


@method_decorator(group_required("Headteacher"), name='dispatch')
class HeadTeacherHomeView(TemplateView):
    """
    Head teacher home view.
    """
    template_name = 'study_base/headteacher_home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['studentgroup_list'] = StudentGroup.objects.all()
        context['modules'] = TestModule.objects.all()
        return context


@method_decorator(group_required("Headteacher"), name='dispatch')
class HeadGroupDetailView(DetailView):
    """
    Group detail view for headteachers.
    """
    model = StudentGroup
    template_name = 'study_base/group_detail_head.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tests'] = self.get_object().plannedtest_set.all()
        return context


@method_decorator(group_required("Headteacher"), name='dispatch')
class TeacherDetailView(DetailView):
    """
    Teacher detail view.
    """
    model = get_user_model()
    template_name = 'study_base/teacher_detail.html'

    def get_queryset(self):
        return get_object_or_404(Group, name="Teacher").user_set.all()
        
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['studentgroup_list'] = self.get_object().group_teacher.all()
        return context


@method_decorator(group_required("Headteacher"), name='dispatch')
class ModuleDetailView(DetailView):
    """
    Module detail view
    """
    model = TestModule
    template_name = 'study_base/module_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = self.get_object().testtask_set.all()
        return context


@method_decorator(group_required("Headteacher"), name='dispatch')
class TaskDetailView(DetailView):
    """
    Task detail view
    """
    model = TestTask
    template_name = 'study_base/task_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        singlechoice = TestTaskSingleChoice.objects.filter(pk=self.get_object().id).exists()
        multiplechoice = TestTaskMultipleChoice.objects.filter(pk=self.get_object().id).exists()
        context['singlechoice'] = singlechoice
        context['multiplechoice'] = multiplechoice
        if singlechoice:
            context['choices'] = self.get_object().testtasksinglechoice.testtasksinglechoiceitem_set.all()
        elif multiplechoice:
            context['choices'] = self.get_object().testtaskmultiplechoice.testtaskmultiplechoiceitem_set.all()
        return context


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
    if PlannedTestManual.objects.filter(pk=test_id).exists():
        return take_test_manual(request, test_id)
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


def take_test_manual(request, test_id):
    """
    Take manual test view.
    """
    test = get_object_or_404(PlannedTestManual, pk=test_id)
    tasks = test.tasks.all()
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
        raise Http404(_("Wrong task number"))
    task = attempt.tasks.all()[task_num]
    if TestTaskSingleChoice.objects.filter(id=task.id).exists():
        return take_test_task_single_choice(request, attempt, task, task_num)
    if TestTaskMultipleChoice.objects.filter(id=task.id).exists():
        return take_test_task_multiple_choice(request, attempt, task, task_num)
    if TestTaskText.objects.filter(id=task.id).exists():
        return take_test_task_text(request, attempt, task, task_num)
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


def take_test_task_text(request, attempt, task, task_num):
    """
    Test task text view.
    """
    if request.method == 'POST':
        form = TakeTestTaskTextForm(request.POST)
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
        form = TakeTestTaskTextForm()
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
        elif TestTaskMultipleChoice.objects.filter(id=task.id).exists():
            if assert_test_task_multiple_choice(attempt_task.task, attempt_task.answer):
                right += 1
        elif TestTaskText.objects.filter(id=task.id).exists():
            if assert_test_task_text(attempt_task.task, attempt_task.answer):
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


def assert_test_task_text(task, answer):
    """
    Checks if answer is right in text task
    """
    return task.testtasktext.answer == answer


@method_decorator(group_required("Student"), name='dispatch')
class TestAttemptResultsView(DetailView):
    """
    Show test attempt results.
    """
    model = TestAttempt
    template_name = 'study_base/attempt_results.html'


@method_decorator(group_required("Student"), name='dispatch')
class PlannedTestAttemptsView(DetailView):
    """
    Show test attempts of student.
    """
    model = PlannedTest
    template_name = 'study_base/attempt_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['attempts'] = self.get_object().testattempt_set.filter(student=self.request.user)
        return context
