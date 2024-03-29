# Generated by Django 4.1.4 on 2023-06-24 20:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('training_calendar', '0004_label_cost_training_is_completed_payment'),
    ]

    operations = [
        migrations.AddField(
            model_name='training',
            name='comment',
            field=models.TextField(blank=True, verbose_name='коментарий'),
        ),
        migrations.AddField(
            model_name='training',
            name='is_burned',
            field=models.BooleanField(default=False, verbose_name='Тренировка сгорела'),
        ),
        migrations.AlterField(
            model_name='training',
            name='is_completed',
            field=models.BooleanField(default=False, verbose_name='Тренировка завершена'),
        ),
    ]
