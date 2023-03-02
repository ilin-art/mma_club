from django import forms
from .models import Task, Comment


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('text', 'signal_date', 'relevance',)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
