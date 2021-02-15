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
