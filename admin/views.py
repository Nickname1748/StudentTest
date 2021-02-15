"""
This module contains views of admin app
"""

from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.urls.base import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.utils.decorators import method_decorator

from study_base.models import StudentGroup
from .decorators import admin_required
from .forms import UpdateRoleForm, GroupCreateForm
from .utils import send_changed_role


@method_decorator(admin_required, name='dispatch')
class MainView(TemplateView):
    """
    Admin panel main page.
    """
    template_name = 'admin/admin.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['unknown_users'] = get_user_model().objects.filter(groups__name='Unknown')[:10]
        context['groups'] = StudentGroup.objects.all()[:10]
        return context


@admin_required
def user_details(request, user_id):
    """
    Page with full information about the new user
    """
    if request.method == 'POST':
        form = UpdateRoleForm(request.POST)
        if form.is_valid():
            user = get_object_or_404(get_user_model(), pk=user_id)
            user.groups.clear()
            group = Group.objects.get_or_create(name=form.cleaned_data['role'])
            user.groups.add(group[0])
            send_changed_role(form.cleaned_data['role'], user.email)

        return redirect(request.path)
    else:
        form = UpdateRoleForm()
        # try:
        #     user = User.objects.get(pk = user_id)
        # except User.DoesNotExist:
        #     raise Http404("Данного пользователя не существует")
        user = get_object_or_404(get_user_model(), pk=user_id)
        context = {}
        context['user'] = user
        if user.groups.filter(name = 'Unknown').exists():
            context['role'] = 'Неподтверждённый'
        elif user.groups.filter(name = 'Student').exists():
            context['role'] = 'Ученик'
        elif user.groups.filter(name = 'Teacher').exists():
            context['role'] = 'Преподаватель'
        elif user.groups.filter(name = 'Headteacher').exists():
            context['role'] = 'Администратор учебного процесса'
        context['form'] = form
    return render(request, 'admin/user_details.html', context=context)


@method_decorator(admin_required, name='dispatch')
class GroupDetailView(DetailView):
    """
    Group detail view.
    """
    model = StudentGroup
    template_name = 'admin/group_detail.html'


@method_decorator(admin_required, name = 'dispatch')
class UserListView(ListView):
    """
    User list view.
    """
    model = get_user_model()
    template_name = 'admin/user_list.html'
    paginate_by = 10

    def get_queryset(self):
        role = self.request.GET.get('role', '')
        queryset = super().get_queryset()
        if role != '':
            queryset = queryset.filter(groups__name=role)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['role'] = self.request.GET.get('role', '')
        return context


@method_decorator(admin_required, name='dispatch')
class GroupListView(ListView):
    """
    Group list view.
    """
    model = StudentGroup
    template_name = "admin/group_list.html"
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        queryset = super().get_queryset()
        if query != '':
            queryset = queryset.filter(name__icontains = query)
        return queryset


@method_decorator(admin_required, name='dispatch')
class StudentGroupCreateView(CreateView):
    """
    Student group create view.
    """
    model = StudentGroup
    template_name = 'admin/group_form.html'
    form_class = GroupCreateForm
    success_url = reverse_lazy('admin:group_list')


@method_decorator(admin_required, name='dispatch')
class StudentGroupUpdateView(UpdateView):
    """
    Student group update view.
    """
    model = StudentGroup
    template_name = 'admin/group_form.html'
    form_class = GroupCreateForm
    success_url = reverse_lazy('admin:group_list')
