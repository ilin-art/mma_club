from django.contrib.auth import views
from .views import SignUp, profile
from django.urls import path

app_name = 'users'

urlpatterns = [
    path(
      'profile/<str:username>/',
      profile,
      name='profile'
    ),
    path(
      'logout/',
      views.LogoutView.as_view(template_name='users/logged_out.html'),
      name='logout'
    ),
    # Полный адрес страницы регистрации - auth/signup/,
    # но префикс auth/ обрабатывется в головном urls.py
    path(
        'signup/',
        SignUp.as_view(),
        name='signup'
    ),
    path(
        'login/',
        views.LoginView.as_view(template_name='users/login.html'),
        name='login'
    ),
    path(
        'password_change/',
        views.PasswordChangeView.as_view(template_name='users/password_change.html'),
        name='password_change'
    ),
    path(
        'password_change/done/',
        views.PasswordChangeDoneView.as_view(template_name='users/password_change_done.html'),
        name='password_change_done'
    ),
    path(
        'password_reset/',
        views.PasswordResetView.as_view(template_name='users/password_reset.html'),
        name='password_reset'
    ),
    path(
        'password_reset/done/',
        views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
        name='password_reset_complete'
    ),
    path(
        'reset/<uidb64>/<token>/',
        views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),
        name='password_reset_confirm'
    ),
    path(
        'reset/done/',
        views.PasswordResetCompleteView.as_view(template_name='users/password_reset_done.html'),
        name='password_reset_done'
    ),
]
