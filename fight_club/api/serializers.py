from rest_framework import serializers

from training_calendar.models import Label, Training, Payment
from users.models import User, Profile, TrainingCount
from tasks.models import Task, Comment
from datetime import datetime
import base64
from django.core.files.base import ContentFile
from django.db.models import Count


class LabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Label
        fields = ('id', 'name', 'color', 'backgroundColor', 'dragBackgroundColor', 'borderColor', 'cost')


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
        fields = ('id', 'coach', 'coach_name', 'clients', 'label', 'start', 'end', 'is_completed')

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


class TrainingCountSerializer(serializers.ModelSerializer):
    label = LabelSerializer()
    # label_id = serializers.PrimaryKeyRelatedField(queryset=Label.objects.all(), source='label')
    # label = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = TrainingCount
        fields = ('label', 'count')


class UserSerializer(serializers.ModelSerializer):
    registration_date = serializers.SerializerMethodField()
    last_login = serializers.SerializerMethodField()
    # training_counts = TrainingCountSerializer(many=True)
    training_counts = serializers.SerializerMethodField()

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
        
    def get_training_counts(self, obj):
        training_counts = TrainingCount.objects.filter(user=obj)
        return [{"name": training_count.label.name, "count": training_count.count} for training_count in training_counts]
        
        
    class Meta:
        model = User
        fields = ('id', 'full_name', 'email', 'phoneNumber', 'training_counts', 'is_trainer',
                  'is_admin', 'registration_date', 'last_login')


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')  
            ext = format.split('/')[-1]  
            data = ContentFile(base64.b64decode(imgstr), name='photo.' + ext)

        return super().to_internal_value(data)
    

class ProfileSerializer(serializers.ModelSerializer):
    photo = Base64ImageField(required=False, allow_null=True)
    trainings_as_coach = serializers.SerializerMethodField(source='get_trainings_as_coach')
    trainings_as_client = serializers.SerializerMethodField(source='get_trainings_as_client')

    class Meta:
        model = Profile
        fields = ('id', 'user', 'gender', 'birthday', 'height', 'weight', 'photo', 'trainings_as_coach', 'trainings_as_client')

    def get_trainings_as_coach(self, obj):
        trainings = obj.user.trainigs_as_coach.filter(is_completed=True)
        label_counts = trainings.values('label__name').annotate(count=Count('label__name')).order_by('label__name')

        return [{'label': label['label__name'], 'count': label['count']} for label in label_counts]
    
    def get_trainings_as_client(self, obj):
        trainings = obj.user.trainigs_as_client.filter(is_completed=True)
        label_counts = trainings.values('label__name').annotate(count=Count('label__name')).order_by('label__name')

        return [{'label': label['label__name'], 'count': label['count']} for label in label_counts]

    def update(self, instance, validated_data):
        # Удаление старого фото перед сохранением нового
        old_photo = instance.photo
        if 'photo' in validated_data and old_photo:
            old_photo.delete(save=False)

        return super().update(instance, validated_data)


class TaskSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.full_name', read_only=True)

    class Meta:
        model = Task
        fields = ('id', 'user', 'text', 'signal_date', 'relevance', 'past', 'now', 'future')


class CommentSerializer(serializers.ModelSerializer):
    comment_to = serializers.CharField(source='task.user', read_only=True)
    author_name = serializers.CharField(source='author.full_name', read_only=True)
    
    class Meta:
        model = Comment
        fields = ('id', 'task', 'comment_to', 'text', 'author', 'author_name', 'created')


class PaymentSerializer(serializers.ModelSerializer):
    # training_label = serializers.CharField(source='training_label.name', read_only=True)


    class Meta:
        model = Payment
        fields = ('id', 'user', 'amount', 'payment_date', 'payment_method', 'training_label')
        extra_kwargs = {
            'user': {'required': True},
            'amount': {'required': True},
            'payment_method': {'required': True},
            'training_label': {'required': True},
        }
