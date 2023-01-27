from django import forms
from .models import Task, Comment


#  создадим собственный класс для формы регистрации
#  сделаем его наследником предустановленного класса UserCreationForm
class TaskForm(forms.ModelForm):
    class Meta:
        # укажем модель, с которой связана создаваемая форма
        model = Task
        # укажем, какие поля должны быть видны в форме и в каком порядке
        fields = ('text', 'signal_date', 'relevance',)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
