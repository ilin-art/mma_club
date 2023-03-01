from rest_framework.decorators import api_view  # Импортировали декоратор
from rest_framework.response import Response  # Импортировали класс Response
from rest_framework import status, viewsets

from .serializers import LabelSerializer, TrainingSerializer, UserSerializer, TrainingNameSerializer

from training_calendar.models import Label, Training

from users.models import User

@api_view(['GET', 'POST'])  # Разрешены только POST- и GET-запросы
def label_list(request):
    # # В случае POST-запроса добавим список записей в БД
    # if request.method == 'POST':
    #     serializer = LabelSerializer(data=request.data, many=True)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # В случае GET-запроса возвращаем список всех котиков
    labels = Label.objects.all()
    serializer = LabelSerializer(labels, many=True)
    return Response(serializer.data)


# @api_view(['GET', 'POST'])  # Разрешены только POST- и GET-запросы
# def trainings_list(request):
#     # В случае POST-запроса добавим список записей в БД
#     if request.method == 'POST':
#         serializer = TrainingSerializer(data=request.data, many=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     # В случае GET-запроса возвращаем список всех котиков
#     labels = Training.objects.all()
#     serializer = TrainingSerializer(labels, many=True)
#     return Response(serializer.data)

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