# Student Test System
# Copyright (C) 2020 Andrey Shmaykhel <shmayhel.andrey@gmail.com>,
#                    Alexander Solovyov
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
    path('groups/<uuid:pk>/update/', views.StudentGroupUpdateView.as_view(), name='update_group'),
    path('groups/', views.GroupListView.as_view(), name='group_list'),
    path('groups/create/', views.StudentGroupCreateView.as_view(), name='create_group_form')
]
