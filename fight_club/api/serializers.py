from rest_framework import serializers

from training_calendar.models import Label, Training
from users.models import User


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
        # instance.coach_name = validated_data.get('coach_name', instance.coach_name)
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
    class Meta:
        model = User
        fields = ('full_name', 'email', 'phoneNumber', 'is_trainer', 'is_admin')
