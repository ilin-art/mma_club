from django.contrib import admin

from .models import User, Profile


class ProfileInline(admin.StackedInline):
    model = Profile


class UserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'full_name', 'email', 'phoneNumber', 'registration_date',)
    list_display_links = ('pk', 'full_name',)
    search_fields = ('full_name', 'phoneNumber',)
    inlines = [ProfileInline]

admin.site.register(User, UserAdmin)


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'gender', 'birthday', 'height', 'weight')
    list_display_links = ('pk', 'user',)
    list_filter = ('gender',)

admin.site.register(Profile, ProfileAdmin)
