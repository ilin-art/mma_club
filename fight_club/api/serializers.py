from rest_framework import serializers

from training_calendar.models import Label, Training
from users.models import User


class LabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Label
        fields = ('name', 'color', 'backgroundColor', 'dragBackgroundColor', 'borderColor')


class TrainingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Training
        fields = ('coach', 'client', 'label', 'start', 'end')


class TrainingNameSerializer(serializers.ModelSerializer):
    coach = serializers.SlugRelatedField(read_only=True, slug_field='full_name')
    client = serializers.SlugRelatedField(read_only=True, many=True, slug_field='full_name')
    label = serializers.SlugRelatedField(read_only=True, slug_field='name')
    
    class Meta:
        model = Training
        fields = ('coach', 'client', 'label', 'start', 'end')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('full_name', 'email', 'phoneNumber', 'is_trainer', 'is_admin')
