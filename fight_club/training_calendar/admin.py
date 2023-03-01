from django.contrib import admin

from .models import Label, Training


class LabelAdmin(admin.ModelAdmin):
    # Перечисляем поля, которые должны отображаться в админке
    list_display = ('pk', 'name')
    list_display_links = ('pk', 'name',)

admin.site.register(Label, LabelAdmin)


class TrainingAdmin(admin.ModelAdmin):
    # Перечисляем поля, которые должны отображаться в админке
    list_display = ('pk', 'coach', 'label', 'start', 'end')
    list_display_links = ('pk', 'label',)

admin.site.register(Training, TrainingAdmin)