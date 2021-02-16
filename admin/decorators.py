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
This module contains decorators for admin app
'''

from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.admin.views.decorators import staff_member_required

def admin_required(view_func = None, redirect_field_name = REDIRECT_FIELD_NAME):
    '''
    Decorator checks that user is staff member, 
    redirects to the login page if it is necessary.
    '''
    return staff_member_required(
        view_func = view_func, 
        redirect_field_name=redirect_field_name,
        login_url='auth_base:login'
    )
