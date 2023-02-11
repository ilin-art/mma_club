from django.shortcuts import render, get_object_or_404
from datetime import date

from .models import Task, Comment
from .forms import CommentForm
from .scripts import authorized_only, last_letter


@authorized_only
def tasks(request):    
    template = '../templates/tasks/tasks_index.html'
    task = Task.objects.order_by('signal_date')
    today = date.today()
    count_past = 0
    count_now = 0
    count_future = 0
    for i in task:
        if i.relevance:
            if i.signal_date.date() < today:
                i.past = True
                i.now = False
                i.future = False
                count_past += 1
            elif i.signal_date.date() == today:
                i.past = False
                i.now = True
                i.future = False
                count_now += 1
            else:
                i.past = False
                i.now = False
                i.future = True
                count_future += 1

    past_last_letter = last_letter(count_past)
    now_last_letter = last_letter(count_now)
    future_last_letter = last_letter(count_future)
    
    context = {
        'tasks': task,
        'today': today,
        'count_past': count_past,
        'count_now': count_now,
        'count_future': count_future,
        'past_last_letter': past_last_letter,
        'now_last_letter': now_last_letter,
        'future_last_letter': future_last_letter,
    }
    return render(request, template, context)

@authorized_only
def add_comment(request, task_id):
    template = '../templates/tasks/comment.html'
    task = get_object_or_404(Task, id=task_id)
    form = CommentForm(request.POST or None)
    comments = Comment.objects.order_by('-created')
    context = {
        'form': form,
        'comments': comments,
    }
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.task = task
        comment.save()
    return render(request, template, context)
