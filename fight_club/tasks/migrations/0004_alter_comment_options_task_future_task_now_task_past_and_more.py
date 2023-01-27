# Generated by Django 4.1.4 on 2023-01-27 18:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0003_comment'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'verbose_name': 'Комментарий', 'verbose_name_plural': 'Комментарии'},
        ),
        migrations.AddField(
            model_name='task',
            name='future',
            field=models.BooleanField(default=False, verbose_name='будущие'),
        ),
        migrations.AddField(
            model_name='task',
            name='now',
            field=models.BooleanField(default=False, verbose_name='сегодняшние'),
        ),
        migrations.AddField(
            model_name='task',
            name='past',
            field=models.BooleanField(default=False, verbose_name='просроченные'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='tasks.task', verbose_name='Кому комментарий'),
        ),
    ]
