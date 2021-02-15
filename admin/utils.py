from django.core.mail import send_mail
from django.template.loader import render_to_string

def get_role_name(role):
    if role == 'Student':
        return 'Ученик'
    if role == 'Unknown':
        return 'Неподтверждённый'
    if role == 'Teacher':
        return 'Преподаватель'
    if role == 'Headteacher':
        return 'Администратор учебного процесса'

def send_changed_role(role, email):
    msg = render_to_string('admin/role_changed.txt', {'role': get_role_name(role)})
    return send_mail('Ваша роль сменилась', msg, recipient_list=[email], from_email = None)
