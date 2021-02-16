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
This module contains forms of admin app
"""

from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _

from study_base.models import StudentGroup


class SelectWidget(forms.Select):
    def create_option(self, *args,**kwargs):
        option = super().create_option(*args, **kwargs)
        if not option.get('value'):
            option['attrs']['disabled'] = True
        return option


class UpdateRoleForm(forms.Form):
    role = forms.ChoiceField(
        choices=(
            ('', _('Select role')),
            ("Unknown", _("Unknown")),
            ("Student", _("Student")),
            ("Teacher", _("Teacher")),
            ("Headteacher", _("Headteacher")),
        ),
        widget=SelectWidget,
        label=_("Role")
    )


class GroupCreateForm(forms.ModelForm):
    """
    Create group form.
    """
    class Meta:
        model = StudentGroup
        fields = ['name', 'teacher', 'students']

    name = forms.CharField(max_length = 50, label=_("Name"))
    teacher = forms.ModelChoiceField(
        queryset=get_user_model().objects.filter(groups__name='Teacher'),
        label=_("Teacher"))
    students = forms.ModelMultipleChoiceField(
        queryset = get_user_model().objects.filter(groups__name ='Student'),
        label=_("Students"))
