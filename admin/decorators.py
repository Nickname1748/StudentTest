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