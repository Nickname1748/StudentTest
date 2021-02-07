'''
This module contains views of admin app
'''

from django.http import Http404, JsonResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.exceptions import ObjectDoesNotExist
from django.views import generic
from django.utils.decorators import method_decorator
from .decorators import admin_required
from .models import Group as group_of_students
from auth_base.models import User
from .forms import UpdateRoleForm, CreateGroupForm
from .utils import send_changed_role

@admin_required
def main_page(request):
    '''
    Main page of admin panel
    '''
    context = {}
    context['unknown_users'] = get_user_model().objects.filter(groups__name = 'Unknown')[:10]
    context['groups'] = group_of_students.objects.all()[:10]
    return render(request, 'admin/admin.html', context=context)

@admin_required
def user_details(request, user_id):
    '''
    Page with full information about the new user
    '''
    if request.method == 'POST':
        form = UpdateRoleForm(request.POST)
        if form.is_valid():
            user_id = int(str(request.path).split('/')[-2])
            try:
                user = User.objects.get(pk = user_id)
                user.groups.clear()
                group = Group.objects.get_or_create(name = form.cleaned_data['role'])
                user.groups.add(group[0])
                send_changed_role(form.cleaned_data['role'], user.email)
            except User.DoesNotExist:
                raise Http404("Данного пользователя не существует")

        return HttpResponseRedirect(request.path)
    else:
        form = UpdateRoleForm()
        try:
            user = User.objects.get(pk = user_id)
        except User.DoesNotExist:
            raise Http404("Данного пользователя не существует")
        else:
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

@admin_required
def group_details(request, group_id):
    '''
    Page with full information about the group
    '''
    try:
        group = group_of_students.objects.get(pk = group_id)
    except ObjectDoesNotExist:
        raise Http404("Данной группы не существует")
    else:
        context = {}
        context['group'] = group
    return render(request, "admin/group_detail.html", context = context)

@method_decorator(admin_required, name = 'dispatch')
class UserListView(generic.ListView):
    model = User
    template_name = "admin/user_list.html"
    paginate_by = 10

    def get_queryset(self):
        role = self.request.GET.get('role', '')
        if role != '':
            new_context = User.objects.filter(
                groups__name = role,
            )
        else:
            new_context = User.objects.all()
        return new_context

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['role'] = self.request.GET.get('role', '')
        return context

@method_decorator(admin_required, name = 'dispatch')
class GroupListView(generic.ListView):
    model = group_of_students
    template_name = "admin/group_list.html"
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get("q", None)
        if query:
            new_context = group_of_students.objects.filter(name__icontains = query)
        else:
            new_context = group_of_students.objects.all()
        return new_context

@admin_required
def create_group_view(request):
    if request.method == 'GET':
        form = CreateGroupForm()
    elif request.method == 'POST':
        form = CreateGroupForm(request.POST)
        if form.is_valid():
            new_group = group_of_students(name = form.cleaned_data['name'], teacher = form.cleaned_data['teacher'])
            new_group.save()
            new_group.students.add(*form.cleaned_data['students'])
            return redirect('admin:group_list')
    return render(request, 'admin/group_form.html', {'form':form})