from datetime import date
from django.utils import timezone
from django.db import models
from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import DateRangeFilter
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import generics
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import datetime, time, timedelta
from django.http import JsonResponse
from django.db.models import Q
from django.utils.dateparse import parse_date
import time

from .serializers import LabelSerializer, UserSerializer, TrainingSerializer, ProfileSerializer, TaskSerializer

from training_calendar.models import Label, Training

from users.models import User, Profile
from tasks.models import Task


#Декоратор для измерения скорости выполнения ф-ии
def measure_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Function {func.__name__} execution time: {end_time - start_time} seconds")
        return result
    return wrapper


class UserList(generics.ListCreateAPIView):
    #Создание и получение всех пользователей
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserProfile(generics.RetrieveUpdateAPIView):
    #Получение и обновление профиля
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

@api_view(['GET'])
def label_list(request):
    # Получение меток для календаря
    labels = Label.objects.all()
    serializer = LabelSerializer(labels, many=True)
    return Response(serializer.data)


class TrainingViewSet(viewsets.ModelViewSet):
    #Все операции с тренировками
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

@api_view(['GET'])
def trainers_list(request):
    # Список тренеров
    trainers = User.objects.all()
    queryset = trainers.filter(is_trainer=True)
    serializer = UserSerializer(queryset, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def admins_list(request):
    # Список админов
    admins = User.objects.all()
    queryset = admins.filter(is_admin=True)
    serializer = UserSerializer(queryset, many=True)
    return Response(serializer.data)

# @api_view(['GET'])
# def tasks(request):
#     # Список сегодняшних заметок
#     tasks = Task.objects.order_by('signal_date')
#     today = date.today()
#     count_past = 0
#     count_now = 0
#     count_future = 0
#     for task in tasks:
#         if task.relevance:
#             if task.signal_date.date() < today:
#                 task.past = True
#                 task.now = False
#                 task.future = False
#                 count_past += 1
#             elif task.signal_date.date() == today:
#                 task.past = False
#                 task.now = True
#                 task.future = False
#                 count_now += 1
#             else:
#                 task.past = False
#                 task.now = False
#                 task.future = True
#                 count_future += 1

        
#         serializer = TaskSerializer(tasks, many=True)
#         return Response(serializer.data)

class TaskPastView(generics.ListAPIView):
    serializer_class = TaskSerializer
    
    def get_queryset(self):
        return Task.objects.filter(relevance=True, past=True).order_by('signal_date')
    

class TaskNowView(generics.ListAPIView):
    serializer_class = TaskSerializer
    
    def get_queryset(self):
        return Task.objects.filter(relevance=True, now=True).order_by('signal_date')


class TaskFutureView(generics.ListAPIView):
    serializer_class = TaskSerializer
    
    def get_queryset(self):
        return Task.objects.filter(relevance=True, future=True).order_by('signal_date')


class TaskCountView(APIView):
    @measure_time
    def get(self, request):
        tasks = Task.objects.filter(relevance=True).order_by('signal_date')
        today = date.today()
        count_past = 0
        count_now = 0
        count_future = 0
        for task in tasks:
            if task.signal_date.date() < today:
                count_past += 1
                if task.past != True:
                    task.past = True
                    task.now = False
                    task.future = False
                    task.save()
            elif task.signal_date.date() == today:
                count_now += 1
                if task.now != True:
                    task.past = False
                    task.now = True
                    task.future = False
                    task.save()
            elif task.signal_date.date() > today:
                count_future += 1
                if task.future != True:
                    task.past = False
                    task.now = False
                    task.future = True
                    task.save()
        return Response({'count_past': count_past, 'count_now': count_now, 'count_future': count_future})

