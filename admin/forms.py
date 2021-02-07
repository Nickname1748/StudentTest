from django import forms
from django.contrib.auth import get_user_model

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
            ('', 'Выберите роль'),
            ("Unknown", "Неподтверждённый"),
            ("Student", "Ученик"),
            ("Teacher", "Преподаватель"),
            ("Headteacher", "Администратор учебного процесса"),
        ),
        widget=SelectWidget,
        label = "Изменить роль"
    )


class GroupCreateForm(forms.ModelForm):
    """
    Create group form.
    """
    class Meta:
        model = StudentGroup
        fields = ['name', 'teacher', 'students']

    name = forms.CharField(max_length = 50, label=("Название"))
    teacher = forms.ModelChoiceField(
        queryset=get_user_model().objects.filter(groups__name = 'Teacher'),
        label=("Преподаватель"))
    students = forms.ModelMultipleChoiceField(
        queryset = get_user_model().objects.filter(groups__name = 'Student'),
        label=("Ученики"))
