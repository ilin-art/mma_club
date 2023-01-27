from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
from django.utils import timezone

User = get_user_model() 


class Task(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
    )
    text = models.TextField(blank=True, verbose_name = 'пометка')
    signal_date = models.DateTimeField(default=timezone.now, verbose_name = 'дата напоминания')
    relevance = models.BooleanField(default=False, verbose_name = 'актуальность')
    past = models.BooleanField(default=False, verbose_name = 'просроченные')
    now = models.BooleanField(default=False, verbose_name = 'сегодняшние')
    future = models.BooleanField(default=False, verbose_name = 'будущие')

    def __str__(self):
        return self.user.full_name

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Заметка'
        verbose_name_plural = 'Заметки'


class Comment(models.Model):
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Кому комментарий",
    )
    text = models.TextField(
        'Текст комментария',
        help_text='Введите текст комментария'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comment_posts',
        verbose_name='Автор поста',
    )
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text
