# Generated by Django 4.1.4 on 2022-12-26 15:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0002_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='task',
            options={'ordering': ('-id',), 'verbose_name': 'Заметка', 'verbose_name_plural': 'Заметки'},
        ),
    ]
