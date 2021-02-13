"""
This module contains study urls.
"""

from django.urls import path

from . import views

app_name = 'study_base'

urlpatterns = [
    path('teacher/', views.TeacherHomeView.as_view(), name='teacher_home'),
    path('teacher/plan_test/', views.PlanTestModularView.as_view(), name='plan_test'),
    path('teacher/edit_test/<uuid:pk>/', views.EditTestModularView.as_view(), name='edit_test'),
    path('teacher/create_module/', views.CreateTestModuleView.as_view(), name='create_module'),
    path('teacher/edit_module/<uuid:pk>/', views.EditTestModuleView.as_view(), name='edit_module'),
    path('teacher/create_tasksinglechoice/', views.CreateTestTaskSingleChoiceView.as_view(), name='create_tasksinglechoice'),
    path('teacher/create_taskmultiplechoice/', views.CreateTestTaskMultipleChoiceView.as_view(), name='create_taskmultiplechoice'),
    path('student/', views.StudentHomeView.as_view(), name='student_home'),
    path('student/take_test/<uuid:test_id>/', views.take_test, name='take_test'),
    path('student/take_test_task/<uuid:attempt_id>/<int:task_num>/', views.take_test_task, name='take_test_task'),
    path('student/attempt_results/<uuid:pk>/', views.TestAttemptResultsView.as_view(), name='attempt_results')
]
