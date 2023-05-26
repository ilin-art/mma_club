from django.contrib import admin

from .models import User, Profile, TrainingCount


class ProfileInline(admin.StackedInline):
    model = Profile

class TrainingCountInline(admin.TabularInline):
    model = TrainingCount


class UserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'full_name', 'email', 'phoneNumber', 'registration_date',)
    list_display_links = ('pk', 'full_name',)
    search_fields = ('full_name', 'phoneNumber',)
    inlines = [ProfileInline, TrainingCountInline]

admin.site.register(User, UserAdmin)


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'gender', 'birthday', 'height', 'weight')
    list_display_links = ('pk', 'user',)
    list_filter = ('gender',)

admin.site.register(Profile, ProfileAdmin)

class TrainingCountAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'label', 'count')
    list_display_links = ('pk', 'user',)
    list_filter = ('label', 'user',)

admin.site.register(TrainingCount, TrainingCountAdmin)
