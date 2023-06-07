from django.db import models
from django.conf import settings
# from django.contrib.auth import get_user_model


# User = get_user_model() 

CHOICES_PAY = (
        ('наличные', 'наличные'),
        ('карта', 'карта'),
        ('ссылка', 'ссылка'),
        ('перевод', 'перевод'),
    )

class Label(models.Model):
    name = models.TextField(verbose_name = 'Название метки')
    color = models.TextField(verbose_name = 'Цвет текста для элемента события')
    backgroundColor = models.TextField(verbose_name = 'Цвет фона для элемента события')
    dragBackgroundColor = models.TextField(verbose_name = 'Цвет фона при перетаскивании элемента события')
    borderColor = models.TextField(verbose_name = 'Цвет левой границы элемента события')
    cost = models.IntegerField(verbose_name='Стоимость тренировки')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Метка'
        verbose_name_plural = 'Метки'


class Training(models.Model):
    label = models.ForeignKey(
        Label, related_name='trainigs',
        on_delete=models.SET_NULL,
        verbose_name="Метка",
        null=True,
    )
    coach = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='trainigs_as_coach',
        on_delete=models.SET_NULL,
        verbose_name="тренер",
        null=True,
    )

    client = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='trainigs_as_client',
        verbose_name="клиент",
        null=True,
    )
    start =  models.DateTimeField(verbose_name='Начало тренировки')
    end =  models.DateTimeField(verbose_name='Конец тренировки')
    is_completed = models.BooleanField(default=False, verbose_name='Завершена тренировка')

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Тренировка'
        verbose_name_plural = 'Тренеровки'


class Payment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, verbose_name='Пользователь')
    amount = models.IntegerField(verbose_name='Сумма оплаты')
    payment_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата оплаты')
    payment_method = models.CharField(choices = CHOICES_PAY, max_length=255, verbose_name='Способ оплаты')
    training_label = models.ForeignKey(Label, on_delete=models.SET_NULL, null=True, verbose_name='Вид тренировки')

    def __str__(self):
        return f"{self.user.full_name} - {self.payment_date}"

    class Meta:
        verbose_name = 'Оплата тренировки'
        verbose_name_plural = 'Оплаты тренировок'

class Payment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, verbose_name='Пользователь')
    amount = models.IntegerField(verbose_name='Сумма оплаты')
    payment_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата оплаты', blank=True)
    payment_method = models.CharField(choices=CHOICES_PAY, max_length=255, verbose_name='Способ оплаты')
    training_label = models.ForeignKey(Label, on_delete=models.SET_NULL, null=True, verbose_name='Вид тренировки')

    def __str__(self):
        return f"{self.user.full_name} - {self.payment_date}"

    class Meta:
        verbose_name = 'Оплата тренировки'
        verbose_name_plural = 'Оплаты тренировок'