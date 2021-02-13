"""
This module contains study urls.
"""

from django.urls import path

from . import views

app_name = 'study_base'

urlpatterns = [
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
    path('student/', views.StudentHomeView.as_view(), name='student_home'),
    path('student/take_test/<uuid:test_id>/', views.take_test, name='take_test'),
    path('student/take_test_task/<uuid:attempt_id>/<int:task_num>/', views.take_test_task, name='take_test_task'),
    path('student/attempt_results/<uuid:pk>/', views.TestAttemptResultsView.as_view(), name='attempt_results')
]