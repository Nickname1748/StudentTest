"""
This module contains test views.
"""

from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from django.utils.decorators import method_decorator

from .models import StudentGroup, PlannedTest, TestTaskSingleChoiceItem
from .decorators import group_required
from .forms import (
    PlanTestModularForm, CreateTestModuleForm, CreateTestTaskSingleChoiceForm,
    CreateTestTaskSingleChoiceItemFormSet)


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
            student_group__teacher__username__exact=self.request.user.username)
        return context


@method_decorator(group_required("Teacher"), name='dispatch')
class PlanTestModularView(CreateView):
    """
    Planning modular test view.
    """
    template_name = 'study_base/plan_test.html'
    form_class = PlanTestModularForm
    success_url = reverse_lazy('study_base:teacher_home')


@method_decorator(group_required("Teacher"), name='dispatch')
class CreateTestModuleView(CreateView):
    """
    Creating test module view.
    """
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
            student_group__in=context['studentgroup_list'])
        return context
