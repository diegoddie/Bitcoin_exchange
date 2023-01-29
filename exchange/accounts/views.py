from django.shortcuts import render, redirect
from django import forms
from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from core.models import Wallet
from .forms import CustomUserRegistrationForm, CustomAuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.http import request
from django.contrib.auth.views import PasswordChangeView
from .forms import CustomPasswordChangeForm, MyPasswordResetForm

class RegisterPage(FormView):
    template_name = 'accounts/register.html'
    form_class = CustomUserRegistrationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        form.save()
        user = form.instance
        user.is_active = True
        user.save()
        return super().form_valid(form)

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    authentication_form = CustomAuthenticationForm
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('home')
    
    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.method == 'POST':
            messages.error(self.request, 'Invalid username or password.')
        return response

class CustomPasswordChangeView(PasswordChangeView):
    form_class = CustomPasswordChangeForm
    template_name = 'accounts/password_change.html'
    success_url = reverse_lazy('home')

class PasswordResetViewCustom(PasswordResetView):
    form_class = MyPasswordResetForm
    template_name = 'accounts/password_reset.html'
    email_template_name = 'accounts/password_reset_email.html'
    subject_template_name = 'accounts/password_reset_subject.txt'
    success_url = '/password_reset_done/'

    def form_invalid(self, form):
        messages.error(self.request, "Invalid email address.")
        return super().form_invalid(form)

class PasswordResetDoneViewCustom(PasswordResetDoneView):
    template_name = 'accounts/password_reset_done.html'

class PasswordResetConfirmViewCustom(PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'

class PasswordResetCompleteViewCustom(PasswordResetCompleteView):
    template_name = 'accounts/password_reset_complete.html'