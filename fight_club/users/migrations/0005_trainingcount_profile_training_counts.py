# Generated by Django 4.1.4 on 2023-05-24 06:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('training_calendar', '0004_label_cost_training_is_completed_payment'),
        ('users', '0004_alter_profile_photo'),
    ]

    operations = [
        migrations.CreateModel(
            name='TrainingCount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField(default=0, verbose_name='Количество тренировок')),
                ('label', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='training_calendar.label', verbose_name='Метка')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.profile', verbose_name='Профиль')),
            ],
            options={
                'verbose_name': 'Количество тренировок',
                'verbose_name_plural': 'Количество тренировок',
            },
        ),
        migrations.AddField(
            model_name='profile',
            name='training_counts',
            field=models.ManyToManyField(related_name='trainigs_as_coach', through='users.TrainingCount', to='training_calendar.label', verbose_name='Количество тренировок'),
        ),
    ]
