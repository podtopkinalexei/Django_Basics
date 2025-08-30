from django.conf import settings
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_POST
from django.views.generic import CreateView

from .forms import UserRegistrationForm, UserLoginForm
from .models import User


class RegisterView(CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        response = super().form_valid(form)

        try:
            subject = _('Добро пожаловать на сайт "Магазин смартфонов"')
            message = _(
                'Благодарим за регистрацию! Теперь вы имеете полный доступ к контенту на нашем сайте "Магазин смартфонов"')
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [form.instance.email]

            send_mail(subject, message, from_email, recipient_list)
        except Exception as e:
            messages.warning(self.request,
                             _('Регистрация прошла успешно, но не удалось отправить приветственное письмо.'))

        return response


class CustomLoginView(LoginView):
    form_class = UserLoginForm
    template_name = 'users/login.html'

    def get_success_url(self):
        return reverse_lazy('catalog:index')


@login_required
def profile_view(request):
    return render(request, 'users/profile.html')


@login_required
def profile_edit_view(request):
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.phone_number = request.POST.get('phone_number', '')
        user.country = request.POST.get('country', '')

        if 'avatar' in request.FILES:
            user.avatar = request.FILES['avatar']

        user.save()
        messages.success(request, _('Профиль успешно обновлен!'))
        return redirect('users:profile')

    return render(request, 'users/profile_edit.html')


@login_required
@require_POST
def remove_avatar_view(request):
    user = request.user
    if user.avatar:
        user.avatar.delete(save=False)
        user.avatar = None
        user.save()
        messages.success(request, _('Аватар успешно удален!'))
    return redirect('users:profile_edit')



def custom_logout(request):
    logout(request)
    return redirect('catalog:index')