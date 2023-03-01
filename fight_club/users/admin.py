from django.contrib import admin

from .models import User, Profile



#Для совместного отображения профиля в ползователе
class ProfileInline(admin.StackedInline):
    model = Profile


class UserAdmin(admin.ModelAdmin):
    # Перечисляем поля, которые должны отображаться в админке
    list_display = ('pk', 'full_name', 'email', 'phoneNumber', 'registration_date',)
    list_display_links = ('pk', 'full_name',)
    # Добавляем интерфейс для поиска по тексту постов
    search_fields = ('full_name', 'phoneNumber',)
    inlines = [ProfileInline]

admin.site.register(User, UserAdmin)


class ProfileAdmin(admin.ModelAdmin):
    # Перечисляем поля, которые должны отображаться в админке
    list_display = ('pk', 'user', 'gender', 'birthday', 'height', 'weight')
    list_display_links = ('pk', 'user',)
    list_filter = ('gender',)

admin.site.register(Profile, ProfileAdmin)
