from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView as DefaultLoginView, LogoutView
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DetailView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from accounts.forms import RegisterForm
from accounts.models import User


class LoginView(SuccessMessageMixin, DefaultLoginView):
    """Login user view"""
    template_name = 'accounts/login.html'
    success_message = 'Pomyślnie zalogowano.'
    redirect_authenticated_user = True


class LogoutView(SuccessMessageMixin, LogoutView):
    """Login user view"""
    success_message = 'Pomyślnie wylogowano.'


class RegisterView(SuccessMessageMixin, CreateView):
    """Register user view"""
    template_name = 'accounts/register.html'
    model = User
    form_class = RegisterForm
    success_url = reverse_lazy('accounts:login')
    success_message = 'Pomyslnie zarejestrowano.'

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy('home-page'))
        return super().dispatch(request, *args, **kwargs)


class ProfileView(DetailView):
    template_name = 'accounts/profile.html'
    model = User

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
