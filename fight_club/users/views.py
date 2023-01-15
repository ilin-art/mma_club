# Импортируем CreateView, чтобы создать ему наследника
from django.views.generic import CreateView

# Функция reverse_lazy позволяет получить URL по параметрам функции path()
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404

# Импортируем класс формы, чтобы сослаться на неё во view-классе
from .forms import CreationForm

from .models import User, Profile


class SignUp(CreateView):
    form_class = CreationForm
    # После успешной регистрации перенаправляем пользователя на главную.
    success_url = reverse_lazy('users:login')
    template_name = 'users/signup.html'


def profile(request, username):
    # Здесь код запроса к модели и создание словаря контекста
    user = get_object_or_404(User, phoneNumber=username)
    name = user.full_name
    email = user.email
    phoneNumber = user.phoneNumber
    registration_date = user.registration_date
    weight = user.profile.weight
    height = user.profile.height
    gender = user.profile.gender
    birthday = user.profile.birthday
    
    context = {
        'name': name,
        'email': email,
        'phoneNumber': phoneNumber,
        'registration_date': registration_date,
        'height': height,
        'gender': gender,
        'birthday': birthday,
        'weight': weight,

    }
    return render(request, 'users/profile.html', context)
