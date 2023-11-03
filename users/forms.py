from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError

from users.models import Profile


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(label='Имя', widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label='Фамилия', widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='Электронная почта', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Пароль', help_text="Пароль должен состоять не менее чем из 8 символов"
                                                          " и не может состоять только из цифр.",
                                widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                  'aria-labelledby': 'passwordHelpBlock'}))
    password2 = forms.CharField(label='Подтвердите пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')

    def clean_email(self):
        user_email = self.cleaned_data['email']
        if User.objects.filter(email=user_email).exists():
            raise ValidationError("Пользователь с таким e-mail уже зарегистрирован.")
        return user_email


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин или E-mail', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class UserProfileForm(UserChangeForm):

    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                               }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                              }))
    username = forms.CharField(disabled=True, widget=forms.TextInput(attrs={'class': 'form-control',
                                                                            }))
    email = forms.CharField(disabled=True, widget=forms.EmailInput(attrs={'class': 'form-control',
                                                                          }))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email',)


class UserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label='Пароль',
                                   widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password1 = forms.CharField(label='Новый пароль',
                                    widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password2 = forms.CharField(label='Подтверждение пароля',
                                    widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class ImageForm(forms.ModelForm):
    image = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control',
                                                           }), required=True, label='Аватар')

    class Meta:
        model = Profile
        fields = ['image']


