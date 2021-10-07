from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.shortcuts import render

# Create your views here.
from admins.forms import UserAdminRegisterForm, UserAdminProfileForm
from geekshop.mixin import CustomDispatchMixin
from users.models import User


def index(request):
    return render(request, 'admins/admin.html')


class UserListView(ListView):
    model = User
    template_name = 'admins/admin-users-read.html'

    # context_object_name = 'users'

    def get_context_data(self, *args, object_list=None, **kwargs):
        content = super(UserListView, self).get_context_data(**kwargs)
        content['title'] = 'Admin | user'
        return content


class UserCreateView(CreateView, CustomDispatchMixin):
    model = User
    template_name = 'admins/admin-users-create.html'
    form_class = UserAdminRegisterForm
    success_url = reverse_lazy('admins:admins_user')

    def get_context_data(self, *args, object_list=None, **kwargs):
        content = super(UserCreateView, self).get_context_data(**kwargs)
        content['title'] = 'Admin | Create user'
        return content


class UserUpdateView(UpdateView, CustomDispatchMixin):
    model = User
    template_name = 'admins/admin-users-update-delete.html'
    form_class = UserAdminProfileForm
    success_url = reverse_lazy('admins:admins_user')

    def get_context_data(self, *args, object_list=None, **kwargs):
        content = super(UserUpdateView, self).get_context_data(**kwargs)
        content['title'] = 'Admin | Update user'
        return content


class UserDeleteView(DeleteView):
    model = User
    template_name = 'admins/admin-users-update-delete.html'
    success_url = reverse_lazy('admins:admins_user')

    # def __init__(self, **kwargs):
    # """   Это PyCharm сам создал когда я исправлял синтаксис для PEP-8, но это не работает"""
    #     super().__init__(kwargs)
    #     self.object = self.get_object()

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super(UserDeleteView, self).dispatch(request, *args, **kwargs)

    def delete(self, *args, **kwargs):
        self.object = self.get_object()

        if self.object.is_active == False:
            self.object.is_active = True

        else:
            self.object.is_active = False

        self.object.save()
        return HttpResponseRedirect(self.get_success_url())
