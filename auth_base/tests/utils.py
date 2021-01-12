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
