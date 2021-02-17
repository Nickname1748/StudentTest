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
This module contains study urls.
"""

from django.urls import path

from . import views

app_name = 'study_base'

urlpatterns = [
    path('', views.index_view, name='index'),
    path('teacher/', views.TeacherHomeView.as_view(), name='teacher_home'),
    path('teacher/edit_test/<uuid:test_id>/', views.edit_test, name='edit_test'),
    path('teacher/plan_test_modular/', views.PlanTestModularView.as_view(), name='plan_test_modular'),
    path('teacher/edit_test_modular/<uuid:pk>/', views.EditTestModularView.as_view(), name='edit_test_modular'),
    path('teacher/plan_test_manual/', views.PlanTestManualView.as_view(), name='plan_test_manual'),
    path('teacher/edit_test_manual/<uuid:pk>/', views.EditTestManualView.as_view(), name='edit_test_manual'),
    path('teacher/create_module/', views.CreateTestModuleView.as_view(), name='create_module'),
    path('teacher/edit_module/<uuid:pk>/', views.EditTestModuleView.as_view(), name='edit_module'),
    path('teacher/create_tasksinglechoice/', views.CreateTestTaskSingleChoiceView.as_view(), name='create_tasksinglechoice'),
    path('teacher/create_taskmultiplechoice/', views.CreateTestTaskMultipleChoiceView.as_view(), name='create_taskmultiplechoice'),
    path('teacher/create_tasktext/', views.CreateTestTaskTextView.as_view(), name='create_tasktext'),
    path('teacher/planned_test_results/<uuid:pk>/', views.PlannedTestDetailView.as_view(), name='planned_test_results'),
    path('teacher/group/<uuid:pk>/', views.GroupDetailView.as_view(), name='group_detail'),
    path('headteacher/', views.HeadTeacherHomeView.as_view(), name='headteacher_home'),
    path('headteacher/teacher/<int:pk>/', views.TeacherDetailView.as_view(), name='teacher_detail'),
    path('headteacher/group/<uuid:pk>/', views.HeadGroupDetailView.as_view(), name='group_detail_head'),
    path('headteacher/module/<uuid:pk>/', views.ModuleDetailView.as_view(), name='module_detail'),
    path('headteacher/task/<uuid:pk>/', views.TaskDetailView.as_view(), name='task_detail'),
    path('student/', views.StudentHomeView.as_view(), name='student_home'),
    path('student/take_test/<uuid:test_id>/', views.take_test, name='take_test'),
    path('student/take_test_task/<uuid:attempt_id>/<int:task_num>/', views.take_test_task, name='take_test_task'),
    path('student/attempt_results/<uuid:pk>/', views.TestAttemptResultsView.as_view(), name='attempt_results'),
    path('student/attempt_list/<uuid:pk>/', views.PlannedTestAttemptsView.as_view(), name='attempt_list')
]
