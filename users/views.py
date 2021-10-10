from django.contrib.auth.views import LogoutView, LoginView
from django.shortcuts import render, HttpResponseRedirect, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.views.generic import FormView, UpdateView

from baskets.models import Basket
from geekshop.mixin import BaseClassContextMixin, UserDispatchMixin
from users.forms import UserLoginForm, UserRegisterForm, UserProfileForm


# Create your views here.
from users.models import User


class LoginListView(LoginView, BaseClassContextMixin):
    template_name = 'users/login.html'
    form_class = UserLoginForm
    title = 'Geekshop - Autorisation'


# def login(request):
#     if request.method == 'POST':
#         form = UserLoginForm(data=request.POST)
#
#         if form.is_valid():
#             username = request.POST['username']
#             password = request.POST['password']
#             user = auth.authenticate(username=username, password=password)
#
#             if user.is_active:
#                 auth.login(request, user)
#                 return HttpResponseRedirect(reverse('index'))
#
#     else:
#         form = UserLoginForm()
#
#     content = {
#         "title": "Geekshop - Autorisation",
#         'form': form
#     }
#     return render(request, 'users/login.html', content)

class RegisterListView(FormView, BaseClassContextMixin):
    model = User
    template_name = 'users/register.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login')
    title = "Geekshop - Registration"

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'You have successfully registered')
            return redirect(self.success_url)
        return redirect(self.success_url)


# def register(request):
#     if request.method == 'POST':
#         form = UserRegisterForm(data=request.POST)
#
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'You success registered !!!')
#             return HttpResponseRedirect(reverse('users:login'))
#
#     else:
#         form = UserRegisterForm()
#
#     content = {
#         'title': "Geekshop - Registration",
#         'form': form
#     }
#     return render(request, 'users/register.html', content)


class ProfileFormView(UpdateView, BaseClassContextMixin, UserDispatchMixin):
    model = User
    template_name = 'users/profile.html'
    form_class = UserProfileForm
    success_url = reverse_lazy('index')
    title = "Geekshop | Profile"

    def get_object(self, queryset=None):
        return get_object_or_404(User, pk=self.request.user.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['baskets'] = Basket.objects.filter(user=self.request.user)
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST, files=request.FILES, instance=self.get_object())

        if form.is_valid():
            form.save()
            messages.success(request, 'You successfully logged')
            return redirect(self.success_url)

        return redirect(self.success_url)


# @login_required
# def profile(request):
#     if request.method == 'POST':
#         form = UserProfileForm(data=request.POST, instance=request.user, files=request.FILES)
#
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'You success logged in !!!')
#             return HttpResponseRedirect(reverse('users:profile'))
#
#         else:
#             messages.error(request, 'Profile is not save !')
#
#     baskets = Basket.objects.filter(user=request.user)
#
#     content = {
#         'title': 'Geekshop - profile',
#         'form': UserProfileForm(instance=request.user),
#         'baskets': baskets,
#     }
#     return render(request, 'users/profile.html', content)


class Logout(LogoutView):
    template_name = 'mainapp/index.html'

# def logout(request):
#     auth.logout(request)
#     return HttpResponseRedirect(reverse('index'))
