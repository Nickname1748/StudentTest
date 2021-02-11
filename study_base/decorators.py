"""
This module contains decorators for study_base app.
"""

from django.contrib.auth.decorators import user_passes_test


def group_required(*group_names):
    """
    Decorator for views that checks that the user is a member of given
    group, redirecting to the login page if necessary.
    """

    def in_group(user):
        return user.is_active and (
            user.is_superuser
            or bool(user.groups.filter(name__in=group_names)))

    return user_passes_test(in_group)
