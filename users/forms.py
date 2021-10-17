import hashlib
import random

from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django import forms
from users.models import User


class UserLoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Please entered username'
        self.fields['password'].widget.attrs['placeholder'] = 'Please entered password'
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control py-4'


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'age', 'first_name', 'last_name', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Please entered name user'
        self.fields['email'].widget.attrs['placeholder'] = 'Please entered email'
        self.fields['first_name'].widget.attrs['placeholder'] = 'Please entered name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Please entered last_name'
        self.fields['password1'].widget.attrs['placeholder'] = 'Please entered password'
        self.fields['password2'].widget.attrs['placeholder'] = 'Please confirm the password'
        self.fields['age'].widget.attrs['placeholder'] = 'Please entered your age'
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control py-4'

    def save(self, commit=True):
        user = super(UserRegisterForm, self).save()
        if User.objects.get(email=user.email):
            raise ValueError('Такой email уже есть')

        user.is_active = False
        salt = hashlib.sha1(self.username.encode('utf8')).hexdigest()[:6]
        user.activation_key = hashlib.sha1((user.email + salt).encode('utf8')).hexdigest()
        user.save()
        return user


class UserProfileForm(UserChangeForm):
    image = forms.ImageField(widget=forms.FileInput(), required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'age', 'first_name', 'last_name', 'image')

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['readonly'] = True
        self.fields['email'].widget.attrs['readonly'] = True

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control py-4'
        self.fields['image'].widget.attrs['class'] = 'custom-file-input'

    # def clean_image(self):
    #     data = self.cleaned_data['image']
    #     if data.size > 1024 * 1024:
    #         raise ValueError('The file is too large')
    #     return data
