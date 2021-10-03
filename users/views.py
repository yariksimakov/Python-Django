from django.shortcuts import render, HttpResponseRedirect
from django.contrib import auth, messages
from django.urls import reverse

from baskets.models import Basket
from users.forms import UserLoginForm, UserRegisterForm, UserProfileForm
from django.contrib.auth.decorators import login_required
# Create your views here.


def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)

        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)

            if user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('index'))

    else:
        form = UserLoginForm()

    context = {
        "title": "Geekshop - Autorisation",
        'form': form
    }
    return render(request, 'users/login.html', context)


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(data=request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'You success registered !!!')
            return HttpResponseRedirect(reverse('users:login'))

    else:
        form = UserRegisterForm()

    context = {
        'title': "Geekshop - Registration",
        'form': form
    }
    return render(request, 'users/register.html', context)


@login_required
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(data=request.POST, instance=request.user, files=request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request, 'You success logged in !!!')
            return HttpResponseRedirect(reverse('users:profile'))

        else:
            messages.error(request, 'Profile is not save !')

    baskets = Basket.objects.filter(user=request.user)
    total_sum = sum(basket.sum() for basket in baskets)

    context = {
        'title': 'Geekshop - profile',
        'form': UserProfileForm(instance=request.user),
        'baskets': baskets,
        'total_sum':total_sum,
    }
    return render(request, 'users/profile.html', context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))
