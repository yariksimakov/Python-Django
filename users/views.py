from django.conf import settings
from django.contrib.auth.views import LogoutView, LoginView
from django.core.mail import send_mail
from django.shortcuts import render, HttpResponseRedirect, redirect, get_object_or_404
from django.contrib import messages, auth
from django.urls import reverse, reverse_lazy
from django.views.generic import FormView, UpdateView

from geekshop.mixin import BaseClassContextMixin, UserDispatchMixin
from users.forms import UserLoginForm, UserRegisterForm, UserProfileForm, UserProfileEditForm

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
        try:
            if form.is_valid():
                user = form.save()
                if send_verify_link(user):
                    messages.success(request, 'You have successfully registered')
                return redirect(self.success_url)
            return redirect(self.success_url)
        except Exception as err:
            messages.error(request, err)
            return redirect('users:register')


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


class ProfileFormView(UpdateView, UserDispatchMixin):
    model = User
    template_name = 'users/profile.html'
    form_class = UserProfileForm
    success_url = reverse_lazy('index')
    title = "Geekshop | Profile"

    def get_object(self, queryset=None):
        return get_object_or_404(User, pk=self.request.user.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = UserProfileEditForm(instance=self.request.user.userprofile)
        return context

    def post(self, request, *args, **kwargs):
        # form = self.form_class(data=request.POST, files=request.FILES, instance=self.get_object())
        # profile_form = UserProfileEditForm(data=request.POST, files=request.FILES, instance=request.user)
        form = UserProfileForm(data=request.POST, files=request.FILES, instance=request.user)
        profile_form = UserProfileEditForm(request.POST, instance=request.user.userprofile)
        if form.is_valid() and profile_form.is_valid():
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


def send_verify_link(user):
    verify_link = reverse('users:verify', args=[user.email, user.activation_key])
    title = f'?????? ?????????????????? ?????????????? ???????????? {user.username} ???????????????? ???? ????????????'
    message = f'?????? ?????????????????????????? ?????????????? ???????????? {user.username} ???? ?????????????? \n {settings.DOMAIN_NAME}{verify_link}'
    return send_mail(title, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)


def verify(request, email, activation_key):
    try:
        user = User.objects.get(email=email)
        if user and user.activation_key == activation_key and not user.is_activation_key_expired():
            user.activation_key = activation_key
            user.activation_key_created = None
            user.is_active = True
            user.save()
            auth.login(request, user)
        return render(request, 'users/verification.html')
    except Exception as err:
        print(err)
        return HttpResponseRedirect(reverse('index'))
