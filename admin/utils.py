"""
This module contains admin utils functions.
"""

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.translation import gettext as _


def send_changed_role(role, email):
    msg = render_to_string('admin/role_changed.txt', {'role': _(role)})
    return send_mail(_('Your role has been changed'), msg, recipient_list=[email], from_email = None)
