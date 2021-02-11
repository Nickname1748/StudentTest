"""
This module contains study urls.
"""

from django.urls import path

from . import views

app_name = 'study_base'

urlpatterns = [
    path('teacher/', views.TeacherHomeView.as_view(), name='teacher_home'),
    path('teacher/plan_test/', views.PlanTestModularView.as_view(), name='plan_test'),
    path('teacher/create_module/', views.CreateTestModuleView.as_view(), name='create_module'),
    path('teacher/create_tasksinglechoice/', views.CreateTestTaskSingleChoiceView.as_view(), name='create_tasksinglechoice'),
    path('student/', views.StudentHomeView.as_view(), name='student_home')
]
