from rest_framework import serializers

from training_calendar.models import Label


class LabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Label
        # В прошлом уроке fields = '__all__' изменили на:
        fields = ('name', 'color', 'backgroundColor', 'dragBackgroundColor', 'borderColor') 