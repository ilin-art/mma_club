from django.shortcuts import render, redirect, get_object_or_404
from datetime import date

from .models import Task
from .forms import CommentForm


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
    task = Task.objects.order_by('signal_date')
    today = date.today()
    past = False
    now = False
    future = False
    for i in task:
        if i.signal_date.date() < today:
            past = True
    # if task.signal_date < today:
    #     past = True
    
    context = {
        'tasks': task,
        'today': today,
        'past': past,
        'now': now,
        'future': future,
    }
    return render(request, template, context)

@authorized_only
def add_comment(request, task_id):
    template = '../templates/tasks/comment.html'
    task = get_object_or_404(Task, id=task_id)
    form = CommentForm(request.POST or None)
    context = {
        'form': form,
    }
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.task = task
        comment.save()
    return render(request, template, context)