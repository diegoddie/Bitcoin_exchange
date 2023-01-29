from .views import CustomPasswordChangeView, CustomLoginView, RegisterPage, PasswordResetViewCustom, PasswordResetDoneViewCustom, PasswordResetConfirmViewCustom, PasswordResetCompleteViewCustom
from . import views
from django.contrib.auth.views import LogoutView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import path

urlpatterns = [
    path('register/', RegisterPage.as_view(), name="register"),
    path('login/', CustomLoginView.as_view(), name="login"),
    path('accounts/login/', CustomLoginView.as_view(), name="login"),
    path('accounts/logout/', LogoutView.as_view(template_name="accounts/logout.html"), name="logout"),
    path('accounts/password_change/', CustomPasswordChangeView.as_view(template_name="accounts/password_change.html"), name="password_change"),
    path('password_reset/', PasswordResetViewCustom.as_view(), name='password_reset'),
    path('password_reset_done/', PasswordResetDoneViewCustom.as_view(), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', PasswordResetConfirmViewCustom.as_view(), name='password_reset_confirm'),
    path('password_reset_complete/', PasswordResetCompleteViewCustom.as_view(), name='password_reset_complete'),
]