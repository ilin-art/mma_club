from django.contrib import admin

from .models import Task, Comment


class TaskAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'signal_date', 'user') 
    search_fields = ('text', 'pk', 'user__username',)
    list_filter = ('signal_date',)
    list_display_links = ('pk', 'text',)

admin.site.register(Task, TaskAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'task', 'author', 'created')
    search_fields = ('text', 'pk',)
    list_filter = ('author',)
    list_display_links = ('pk', 'text',)

admin.site.register(Comment, CommentAdmin)