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
This module contains utilities for testing auth_base app
'''

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

def check_user_in_group(username, group):
    '''
    Checks if user is in group.
    '''
    return (
        Group.objects.get(name=group) in
        get_user_model().objects.get(username = username).groups.all()
    )
