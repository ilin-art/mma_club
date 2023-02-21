from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
from django.utils import timezone

User = get_user_model() 


class Label(models.Model):
    name = models.TextField(verbose_name = 'Название метки')
    color = models.TextField(verbose_name = 'Цвет текста для элемента события')
    backgroundColor = models.TextField(verbose_name = 'Цвет фона для элемента события')
    dragBackgroundColor = models.TextField(verbose_name = 'Цвет фона при перетаскивании элемента события')
    borderColor = models.TextField(verbose_name = 'Цвет левой границы элемента события')

    def __str__(self):
        return self.name

    class Meta:
        # ordering = ('-id',)
        verbose_name = 'Метка'
        verbose_name_plural = 'Метки'


# class Comment(models.Model):
#     task = models.ForeignKey(
#         Task,
#         on_delete=models.CASCADE,
#         related_name="comments",
#         verbose_name="Кому комментарий",
#     )
#     text = models.TextField(
#         'Текст комментария',
#         help_text='Введите текст комментария'
#     )
#     author = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE,
#         related_name='comment_posts',
#         verbose_name='Автор поста',
#     )
#     created = models.DateTimeField(default=timezone.now)

#     class Meta:
#         verbose_name = "Комментарий"
#         verbose_name_plural = 'Комментарии'

#     def __str__(self):
#         return self.text
