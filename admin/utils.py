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

"""
This module contains admin utils functions.
"""

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.translation import gettext as _


def send_changed_role(role, email):
    msg = render_to_string('admin/role_changed.txt', {'role': _(role)})
    return send_mail(_('Your role has been changed'), msg, recipient_list=[email], from_email = None)
