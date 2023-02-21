from django.contrib import admin

from .models import Task, Comment


class TaskAdmin(admin.ModelAdmin):
    # Перечисляем поля, которые должны отображаться в админке
    list_display = ('pk', 'text', 'signal_date', 'user') 
    # Добавляем интерфейс для поиска по тексту постов
    search_fields = ('text', 'pk', 'user__username',)
    # Добавляем возможность фильтрации по дате
    list_filter = ('signal_date',)
    list_display_links = ('pk', 'text',)

admin.site.register(Task, TaskAdmin)


class CommentAdmin(admin.ModelAdmin):
    # Перечисляем поля, которые должны отображаться в админке
    list_display = ('pk', 'text', 'task', 'author', 'created')
    # Добавляем интерфейс для поиска по тексту постов
    search_fields = ('text', 'pk',)
    # Добавляем возможность фильтрации по дате
    list_filter = ('author',)
    list_display_links = ('pk', 'text',)

admin.site.register(Comment, CommentAdmin)