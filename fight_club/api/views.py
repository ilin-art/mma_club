from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets

from .serializers import LabelSerializer, TrainingSerializer, UserSerializer, TrainingNameSerializer

from training_calendar.models import Label, Training

from users.models import User

@api_view(['GET', 'POST'])
def label_list(request):
    labels = Label.objects.all()
    serializer = LabelSerializer(labels, many=True)
    return Response(serializer.data)


class TrainingViewSet(viewsets.ModelViewSet):
    queryset = Training.objects.all()
    serializer_class = TrainingSerializer


@api_view(['GET'])  # Список тренеровок c именами вместо id
def trainings_list_name(request):
    trainings = Training.objects.all()
    serializer = TrainingNameSerializer(trainings, many=True)
    return Response(serializer.data)

@api_view(['GET'])  # Список тренеров
def trainers_list(request):
    trainers = User.objects.all()
    queryset = trainers.filter(is_trainer=True)
    serializer = UserSerializer(queryset, many=True)
    return Response(serializer.data)

@api_view(['GET'])  # Список админов
def admins_list(request):
    admins = User.objects.all()
    queryset = admins.filter(is_admin=True)
    serializer = UserSerializer(queryset, many=True)
    return Response(serializer.data)

@api_view(['GET'])  # Список всех пользователей
def users_list(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)
