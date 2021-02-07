import uuid

from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy

class StudentGroup(models.Model):
    """
    Group of students to test
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name=gettext_lazy('ID')
    )
    name = models.CharField(max_length=255, verbose_name=gettext_lazy('Name'))
    teacher = models.ForeignKey(
        get_user_model(),
        on_delete=models.PROTECT,
        verbose_name=gettext_lazy('Teacher'),
        related_name='group_teacher'
    )
    students = models.ManyToManyField(get_user_model(), related_name='group_students')
