from django.contrib import admin

from .models import Task


class TaskAdmin(admin.ModelAdmin):
    # Перечисляем поля, которые должны отображаться в админке
    list_display = ('pk', 'text', 'pub_date', 'author') 
    # Добавляем интерфейс для поиска по тексту постов
    search_fields = ('text', 'pk', 'author__username',)
    # Добавляем возможность фильтрации по дате
    list_filter = ('pub_date',)


admin.site.register(Task, TaskAdmin)
