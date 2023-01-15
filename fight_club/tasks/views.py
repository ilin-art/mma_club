from django.shortcuts import render, redirect

from .models import Task


def authorized_only(func):
    # Функция-обёртка в декораторе может быть названа как угодно
    def check_user(request, *args, **kwargs):
        # В любую view-функцию первым аргументом передаётся объект request,
        # в котором есть булева переменная is_authenticated,
        # определяющая, авторизован ли пользователь.
        if request.user.is_authenticated:
            # Возвращает view-функцию, если пользователь авторизован.
            return func(request, *args, **kwargs)
        # Если пользователь не авторизован — отправим его на страницу логина.
        return redirect('/auth/login/')        
    return check_user


@authorized_only
def tasks(request):    
    template = '../templates/tasks/tasks_index.html'
    task = Task.objects.order_by('-pub_date')
    context = {
        'tasks': task,
    }
    return render(request, template, context)
