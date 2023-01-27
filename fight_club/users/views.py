# Импортируем CreateView, чтобы создать ему наследника
from django.views.generic import CreateView, View, FormView

# Функция reverse_lazy позволяет получить URL по параметрам функции path()
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404, redirect

# Импортируем класс формы, чтобы сослаться на неё во view-классе
from .forms import CreationForm, ProfileForm
from tasks.forms import TaskForm

from .models import User, Profile
from tasks.models import Task


class SignUp(CreateView):
    form_class = CreationForm
    # После успешной регистрации перенаправляем пользователя на главную.
    success_url = reverse_lazy('users:login')
    template_name = 'users/signup.html'


class ProfileView(View):
    template_name = 'users/profile_edit.html'

    def get(self, request, username, *args, **kwargs):
        user = get_object_or_404(User, phoneNumber=username)
        name = user.full_name
        email = user.email
        phoneNumber = user.phoneNumber
        registration_date = user.registration_date
        weight = user.profile.weight
        height = user.profile.height
        gender = user.profile.gender
        birthday = user.profile.birthday
        profile = get_object_or_404(Profile, user=user)
        task = get_object_or_404(Task, user=user)

        global context

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

        profile_form = ProfileForm(self.request.GET or None, instance=profile)
        task_form = TaskForm(self.request.GET or None, instance=task)
        context['profile_form'] = profile_form
        context['task_form'] = task_form
        return render(request, 'users/profile_edit.html', context)

    def post(self, request, username, *args, **kwargs):
        user = get_object_or_404(User, phoneNumber=username)
        profile = get_object_or_404(Profile, user=user)
        task = get_object_or_404(Task, user=user)
        profile_form = ProfileForm(
            request.POST or None,
            request.FILES or None,
            instance=profile
        )
        task_form = TaskForm(
            request.POST or None,
            request.FILES or None,
            instance=task
        )

        if task_form.is_valid():
            task_form.save()
        if profile_form.is_valid():
            profile_form.save()
            return redirect(request.META.get('HTTP_REFERER','redirect_if_referer_not_found'))
        return render(request, 'users/profile_edit.html', context)


class ProfileFormView(FormView):
    form_class = ProfileForm
    template_name = 'users/profile_edit.html'
    success_url = '/tasks'

    def post(self, request, username, *args, **kwargs):
        profile_form = self.form_class(request.POST or None)
        # answer_form = AnswerForm()
        if profile_form.is_valid():
            profile_form.save()
            return self.render_to_response(
                self.get_context_data(
                success=True
            )
        )
        else:
            return self.render_to_response(
            self.get_context_data(
                    profile_form=profile_form,
    
            )
        )


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

    # form = ProfileForm(instance=user)
    # if form.is_valid():
    #         user = form.save()
    #         return render(request, 'users/profile.html', {'form': form}, context)
    # # И в словаре контекста передаём эту форму в HTML-шаблон
    # return render(request, 'users/profile.html', {'form': form}, context)
    return render(request, 'users/profile.html', context)


# def profile_edit(request, username):
#     # Здесь код запроса к модели и создание словаря контекста
#     user = get_object_or_404(User, phoneNumber=username)
#     name = user.full_name
#     email = user.email
#     phoneNumber = user.phoneNumber
#     registration_date = user.registration_date
#     weight = user.profile.weight
#     height = user.profile.height
#     gender = user.profile.gender
#     birthday = user.profile.birthday
#     profile = get_object_or_404(Profile, user=user)
#     profile_form = ProfileForm(
#             request.POST or None,
#             request.FILES or None,
#             instance=profile
#         )
        
#     context = {
#         'name': name,
#         'email': email,
#         'phoneNumber': phoneNumber,
#         'registration_date': registration_date,
#         'height': height,
#         'gender': gender,
#         'birthday': birthday,
#         'weight': weight,
#         'profile_form': profile_form,
#     }

#     # Проверяем, получен POST-запрос или какой-то другой:
#     if request.method == 'POST':
#         if profile_form.is_valid():
#             # сохраняем объект в базу
#             profile_form.save()
            
#             # Функция redirect перенаправляет пользователя 
#             # на другую страницу сайта, чтобы защититься 
#             # от повторного заполнения формы
#             return render(request, 'users/profile_edit.html', context) 

#         return render(request, 'users/profile_edit.html', context)
#     return render(request, 'users/profile_edit.html', context)
