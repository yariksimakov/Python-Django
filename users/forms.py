from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

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
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Please entered name user'
        self.fields['email'].widget.attrs['placeholder'] = 'Please entered email'
        self.fields['first_name'].widget.attrs['placeholder'] = 'Please entered name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Please entered last_name'
        self.fields['password1'].widget.attrs['placeholder'] = 'Please entered password'
        self.fields['password2'].widget.attrs['placeholder'] = 'Please confirm the password'
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control py-4'