from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required
from .forms import LoginForm, UserRegistrationForm
from .models import UserProfile


class CustomLoginView(LoginView):
    """
    Власне представлення для входу користувача.
    """
    form_class = LoginForm
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True


@method_decorator(staff_member_required, name='dispatch')
class UserRegistrationView(CreateView):
    """
    Представлення для реєстрації нового користувача.
    Доступне тільки для адміністраторів.
    """
    form_class = UserRegistrationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('dashboard:index')

    def form_valid(self, form):
        response = super().form_valid(form)
        # Створюємо профіль користувача з вибраною роллю
        UserProfile.objects.create(
            user=self.object,
            role=form.cleaned_data['role']
        )
        return response


@login_required
def profile_view(request):
    """
    Представлення профілю користувача.
    """
    return render(request, 'accounts/profile.html')


@login_required
def set_active_duty(request):
    """
    Встановлення статусу "на зміні" для користувача.
    """
    if request.method == 'POST':
        status = request.POST.get('active_duty') == 'true'
        profile = request.user.profile
        profile.is_active_duty = status
        profile.save()
    return redirect('accounts:profile')