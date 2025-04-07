from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import UserProfile


class LoginForm(AuthenticationForm):
    """
    Форма для входу користувача в систему.
    """
    username = forms.CharField(
        label="Ім'я користувача",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введіть ім\'я користувача'})
    )
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Введіть пароль'})
    )


class UserRegistrationForm(UserCreationForm):
    """
    Форма для реєстрації нового користувача.
    """
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Введіть email'})
    )
    first_name = forms.CharField(
        label="Ім'я",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введіть ім\'я'})
    )
    last_name = forms.CharField(
        label="Прізвище",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введіть прізвище'})
    )
    username = forms.CharField(
        label="Ім'я користувача",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введіть ім\'я користувача'})
    )
    password1 = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Введіть пароль'})
    )
    password2 = forms.CharField(
        label="Підтвердження пароля",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Підтвердіть пароль'})
    )
    role = forms.ChoiceField(
        label="Роль",
        choices=UserProfile.ROLE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')