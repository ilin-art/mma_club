from django.contrib import admin

from .models import Label


class LabelAdmin(admin.ModelAdmin):
    # Перечисляем поля, которые должны отображаться в админке
    list_display = ('pk', 'name')
    list_display_links = ('pk', 'name',)

admin.site.register(Label, LabelAdmin)
