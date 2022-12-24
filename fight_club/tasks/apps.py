from django.apps import AppConfig


class TasksConfig(AppConfig):
    name = 'tasks'
    # Тут можно указать, например, поле verbose_name 
    # под этим именем приложение будет видно в админке.
    verbose_name = 'Управление заметками'
