"""
This module contains test views.
"""

from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView

from .models import StudentGroup, PlannedTest
from .forms import PlanTestModularForm, CreateTestModuleForm


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


class PlanTestModularView(CreateView):
    """
    Planning modular test view.
    """
    template_name = 'study_base/plan_test.html'
    form_class = PlanTestModularForm
    success_url = reverse_lazy('study_base:teacher_home')

class CreateTestModuleView(CreateView):
    """
    Creating test module view.
    """
    template_name = 'study_base/create_module.html'
    form_class = CreateTestModuleForm
    success_url = reverse_lazy('study_base:teacher_home')


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
