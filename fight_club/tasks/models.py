from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model() 


class Task(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='tasks'
    )

    def __str__(self):
        return self.text

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Заметка'
        verbose_name_plural = 'Заметки'