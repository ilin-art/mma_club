from django.utils import timezone
from django.db import models
from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import DateRangeFilter
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import status
from datetime import datetime, time, timedelta
from django.http import JsonResponse
from django.db.models import Q
from django.utils.dateparse import parse_date

from .serializers import LabelSerializer, UserSerializer, TrainingSerializer

from training_calendar.models import Label, Training

from users.models import User

@api_view(['GET'])
def label_list(request):
    labels = Label.objects.all()
    serializer = LabelSerializer(labels, many=True)
    return Response(serializer.data)


class TrainingViewSet(viewsets.ModelViewSet):
    queryset = Training.objects.all()
    serializer_class = TrainingSerializer
    filter_backends = (DjangoFilterBackend,)
    pagination_class = None
    filterset_fields = {'start': ['gte', 'lte', 'exact']}

    def filter_queryset(self, queryset):
        start_str_gte = self.request.GET.get('start__gte')
        start_str_lte = self.request.GET.get('start__lte')
        start_str_date = self.request.GET.get('start__date')

        if start_str_gte:
            start_gte = datetime.fromisoformat(start_str_gte)
            start_gte = datetime.combine(start_gte, time.min)
            queryset = queryset.filter(start__gte=start_gte)

        if start_str_lte:
            start_lte = datetime.fromisoformat(start_str_lte)
            start_lte = datetime.combine(start_lte, time.max)
            queryset = queryset.filter(start__lte=start_lte)

        if start_str_date:
            start_date = parse_date(start_str_date)
            start_of_day = datetime.combine(start_date, time.min)
            end_of_day = datetime.combine(start_date, time.max)
            queryset = queryset.filter(start__gte=start_of_day, start__lte=end_of_day)
        return queryset

@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])  
def trainings_detail(request, pk):
    try:
        training = Training.objects.get(pk=pk)
    except Training.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = TrainingSerializer(training)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = TrainingSerializer(training, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PATCH':
        serializer = TrainingSerializer(training, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        training.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
@api_view(['GET'])
def trainings_today(request):
    # Получаем все тренировки за текущий день
    trainings = Training.objects.filter(
        start__year=timezone.now().year,
        start__month=timezone.now().month,
        start__day=timezone.now().day
    )
    serializer = TrainingSerializer(trainings, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def trainings_this_week(request):
    # Получаем все тренировки за текущую неделю
    trainings = Training.objects.filter(
        start__year=timezone.now().year,
        start__week=timezone.now().isocalendar()[1]
    )
    serializer = TrainingSerializer(trainings, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def trainings_this_month(request):
    # Получаем все тренировки за текущий месяц
    trainings = Training.objects.filter(
        start__year=timezone.now().year, start__month=timezone.now().month
    )
    serializer = TrainingSerializer(trainings, many=True)
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
