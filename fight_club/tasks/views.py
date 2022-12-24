from django.shortcuts import render

from .models import Task

def tasks(request):    
    template = '../templates/tasks/tasks_index.html'
    task = Task.objects.order_by('-pub_date')
    context = {
        'tasks': task,
    }
    return render(request, template, context)

