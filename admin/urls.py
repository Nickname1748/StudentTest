'''
This module contains admin URLs
'''

from django.urls import path
from . import views

app_name = 'admin'

urlpatterns = [
    #TO ADD: admin/, admin/groups/<group_id> (name = group_detail)
    path('', views.MainView.as_view(), name='admin'),
    path('users/', views.UserListView.as_view(), name='user_list'),
    path('users/<int:user_id>/', views.user_details, name='user_detail'),
    path('groups/<uuid:pk>/', views.GroupDetailView.as_view(), name='group_detail'),
    path('groups/', views.GroupListView.as_view(), name='group_list'),
    path('groups/create/', views.StudentGroupCreateView.as_view(), name='create_group_form')
]