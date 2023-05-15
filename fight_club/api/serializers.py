from rest_framework import serializers

from training_calendar.models import Label, Training
from users.models import User, Profile
from tasks.models import Task
from datetime import datetime


class LabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Label
        fields = ('id', 'name', 'color', 'backgroundColor', 'dragBackgroundColor', 'borderColor')


class ClientSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='get_full_name', required=False)
    id = serializers.IntegerField(source='pk')

    class Meta:
        model = User
        fields = ('id', 'full_name')
        read_only_fields = ('id',)

class TrainingSerializer(serializers.ModelSerializer):
    coach_name = serializers.CharField(source='coach.full_name', read_only=True)
    clients = ClientSerializer(source='client', many=True)

    class Meta:
        model = Training
        fields = ('id', 'coach', 'coach_name', 'clients', 'label', 'start', 'end',)

    def create(self, validated_data):
        clients_data = validated_data.pop('client')
        training = Training.objects.create(**validated_data)
        for client_data in clients_data:
            print(client_data)
            training.client.add(User.objects.get(id=client_data['pk']))
        return training
    
    def update(self, instance, validated_data):
        clients_data = validated_data.pop('client', None)
        
        instance.coach = validated_data.get('coach', instance.coach)
        instance.label = validated_data.get('label', instance.label)
        instance.start = validated_data.get('start', instance.start)
        instance.end = validated_data.get('end', instance.end)

        if clients_data is not None:
            instance.client.clear()
            for client_data in clients_data:
                instance.client.add(User.objects.get(id=client_data['pk']))

        instance.save()
        return instance


class UserSerializer(serializers.ModelSerializer):
    registration_date = serializers.SerializerMethodField()
    last_login = serializers.SerializerMethodField()

    def get_registration_date(self, obj):
        if obj.registration_date:
            return obj.registration_date.strftime('%Y-%m-%d %H:%M')
        else:
            return None

    def get_last_login(self, obj):
        if obj.last_login:
            return obj.last_login.strftime('%Y-%m-%d %H:%M')
        else:
            return None
        
    class Meta:
        model = User
        fields = ('id', 'full_name', 'email', 'phoneNumber', 'is_trainer',
                  'is_admin', 'registration_date', 'last_login')


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('id', 'user', 'gender', 'birthday', 'height', 'weight')


class TaskSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.full_name', read_only=True)

    class Meta:
        model = Task
        fields = ('id', 'user', 'text', 'signal_date', 'relevance', 'past', 'now', 'future')
