from django.contrib import admin

from .models import Label, Training, Payment


class LabelAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name')
    list_display_links = ('pk', 'name',)

admin.site.register(Label, LabelAdmin)


class TrainingAdmin(admin.ModelAdmin):
    list_display = ('pk', 'coach', 'label', 'start', 'end')
    list_display_links = ('pk', 'label',)

admin.site.register(Training, TrainingAdmin)


class PaymentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'amount', 'payment_date', 'payment_method', 'training_label')
    list_display_links = ('pk', 'user',)

admin.site.register(Payment, PaymentAdmin)