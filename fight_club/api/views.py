from datetime import date
from django.utils import timezone
# from django.db import models
# from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend
# from django_filters import DateRangeFilter
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import generics
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import datetime, time, timedelta
# from django.http import JsonResponse
# from django.db.models import Q
from django.utils.dateparse import parse_date
import time
from django.db.models import F

from .serializers import LabelSerializer, UserSerializer, TrainingSerializer,\
ProfileSerializer, TaskSerializer, CommentSerializer, PaymentSerializer

from training_calendar.models import Label, Training, Payment

from users.models import User, Profile, TrainingCount
from tasks.models import Task, Comment


#Декоратор для измерения скорости выполнения ф-ии
def measure_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Function {func.__name__} execution time: {end_time - start_time} seconds")
        return result
    return wrapper


class UserList(generics.ListAPIView):
    # Получение пользователей
    serializer_class = UserSerializer

    def get_queryset(self):
        queryset = User.objects.all()
        full_name = self.request.query_params.get('full_name')
        phone_number = self.request.query_params.get('phoneNumber')
        if full_name:
            queryset = queryset.filter(full_name__icontains=full_name)
        if phone_number:
            queryset = queryset.filter(phoneNumber__icontains=phone_number)

        return queryset


class UserDetail(generics.RetrieveAPIView):
    #Получение одного пользователя по id
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
    filterset_fields = {
        'start': ['gte', 'lte', 'exact'],
        'coach': ['exact'],
        'client': ['exact'],
        'label': ['exact'],
        'is_completed': ['exact'],
    }

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        # Проверяем поле is_completed в данных запроса
        is_completed = serializer.validated_data.get('is_completed')

        # Если поле is_completed присутствует и равно True
        if is_completed is True and instance.is_completed is False:
            # Изменяем поле is_completed в объекте Training
            instance.is_completed = True
            instance.save()

            # Обновляем количество тренировок (count) для соответствующих клиентов в модели TrainingCount
            clients = instance.client.all()
            for client in clients:
                training_count = TrainingCount.objects.get(user=client, label=instance.label)
                training_count.count -= 1
                training_count.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    def filter_queryset(self, queryset):
        start_str_gte = self.request.GET.get('start__gte')
        start_str_lte = self.request.GET.get('start__lte')
        start_str_date = self.request.GET.get('start__date')
        coach_id = self.request.GET.get('coach')
        clients_ids = self.request.GET.getlist('client')
        label_id = self.request.GET.get('label')
        is_completed = self.request.GET.get('is_completed')

        if start_str_gte:
            start_gte = datetime.fromisoformat(start_str_gte)
            start_gte = datetime.combine(start_gte.date(), datetime.min.time())
            queryset = queryset.filter(start__gte=start_gte)

        if start_str_lte:
            start_lte = datetime.fromisoformat(start_str_lte)
            start_lte = datetime.combine(start_lte.date(), datetime.max.time())
            queryset = queryset.filter(start__lte=start_lte)

        if start_str_date:
            start_date = parse_date(start_str_date)
            start_of_day = datetime.combine(start_date, datetime.min.time())
            end_of_day = datetime.combine(start_date, datetime.max.time())
            queryset = queryset.filter(start__gte=start_of_day, start__lte=end_of_day)

        if coach_id:
            queryset = queryset.filter(coach=coach_id)

        if clients_ids:
            queryset = queryset.filter(client__in=clients_ids)

        if label_id:
            queryset = queryset.filter(label=label_id)

        if is_completed == 'true':
            queryset = queryset.filter(is_completed=True)

        return queryset.distinct()
    
    
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


class TaskListView(generics.ListAPIView):
    # Список заметок и создание новой заметки
    serializer_class = TaskSerializer

    def get_queryset(self):
        queryset = Task.objects.all()
        signal_date_str_gte = self.request.GET.get('signal_date__gte')
        signal_date_str_lte = self.request.GET.get('signal_date__lte')
        signal_date_str_date = self.request.GET.get('signal_date__date')

        if signal_date_str_gte:
            signal_date_gte = datetime.fromisoformat(signal_date_str_gte)
            signal_date_gte = datetime.combine(signal_date_gte.date(), datetime.min.time())
            queryset = queryset.filter(signal_date__gte=signal_date_gte)

        if signal_date_str_lte:
            signal_date_lte = datetime.fromisoformat(signal_date_str_lte)
            signal_date_lte = datetime.combine(signal_date_lte.date(), datetime.max.time())
            queryset = queryset.filter(signal_date__lte=signal_date_lte)

        if signal_date_str_date:
            signal_date_date = parse_date(signal_date_str_date)
            start_of_day = datetime.combine(signal_date_date, datetime.min.time())
            end_of_day = datetime.combine(signal_date_date, datetime.max.time())
            queryset = queryset.filter(signal_date__gte=start_of_day, signal_date__lte=end_of_day)

        # Фильтрация по полю "user"
        user = self.request.query_params.get('user')
        if user:
            queryset = queryset.filter(user__full_name__icontains=user)

        # Фильтрация по полю "phone_number"
        phone_number = self.request.query_params.get('phone_number')
        if phone_number:
            queryset = queryset.filter(user__phoneNumber__icontains=phone_number)

        # Фильтрация по полю "signal_date"
        relevance = self.request.query_params.get('relevance')
        if relevance:
            queryset = queryset.filter(relevance=relevance)

        return queryset

    def perform_create(self, serializer):
        serializer.save()


class TaskDetailView(generics.RetrieveUpdateAPIView):
    # Детали заметки и обновление заметки
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    http_method_names = ['get', 'patch']

    def perform_update(self, serializer):
        # Получаем изменяемые поля из запроса
        data = self.request.data
        update_fields = {}

        # Проверяем, является ли поле разрешенным для обновления
        for field in ('text', 'signal_date', 'relevance'):
            if field in data:
                update_fields[field] = data[field]

        # Обновляем только разрешенные поля
        serializer.save(**update_fields)


class TaskPastView(generics.ListAPIView):
    # Список просроченных заметок
    serializer_class = TaskSerializer
    
    def get_queryset(self):
        return Task.objects.filter(relevance=True, past=True).order_by('signal_date')
    

class TaskNowView(generics.ListAPIView):
    # Список сегодняшних заметок
    serializer_class = TaskSerializer
    
    def get_queryset(self):
        return Task.objects.filter(relevance=True, now=True).order_by('signal_date')


class TaskFutureView(generics.ListAPIView):
    # Список будущих заметок
    serializer_class = TaskSerializer
    
    def get_queryset(self):
        return Task.objects.filter(relevance=True, future=True).order_by('signal_date')


class TaskCountView(APIView):
    # Подсчет заметок каждого вида
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


class CommentView(APIView):
    def get(self, request, pk):
        comments = Comment.objects.filter(task_id=pk).order_by('-created')
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def post(self, request, pk):
        request.data['task'] = pk
        request.data['author'] = request.user.id
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PaymentView(APIView):
    def get(self, request):
        queryset = Payment.objects.all()
        payment_date_str = request.GET.get('payment_date')
        payment_date_gte_str = request.GET.get('payment_date__gte')
        payment_date_lte_str = request.GET.get('payment_date__lte')
        if payment_date_str:
            payment_date = datetime.strptime(payment_date_str, '%Y-%m-%d').date()
            start_of_day = datetime.combine(payment_date, datetime.min.time())
            end_of_day = datetime.combine(payment_date, datetime.max.time())
            queryset = queryset.filter(payment_date__gte=start_of_day, payment_date__lte=end_of_day)
        if payment_date_gte_str and payment_date_lte_str:
            payment_date_gte = datetime.strptime(payment_date_gte_str, '%Y-%m-%d').date()
            payment_date_lte = datetime.strptime(payment_date_lte_str, '%Y-%m-%d').date() + timedelta(days=1)
            queryset = queryset.filter(payment_date__range=[payment_date_gte, payment_date_lte])
        # Применяем фильтрацию по полю "user", если параметр указан в запросе
        user_id = request.GET.get('user')
        if user_id:
            queryset = queryset.filter(user=user_id)
        # Применяем фильтрацию по полю "payment_method", если параметр указан в запросе
        payment_method = request.GET.get('payment_method')
        if payment_method:
            queryset = queryset.filter(payment_method=payment_method)
        # Применяем фильтрацию по полю "training_label", если параметр указан в запросе
        training_label_id = request.GET.get('training_label')
        if training_label_id:
            queryset = queryset.filter(training_label=training_label_id)

        serializer = PaymentSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            label_id = request.data['training_label']
            label = Label.objects.get(id=label_id)
            label_cost = label.cost
            label_count = int(request.data['amount'] / label_cost)
            user_id = request.data['user']
            client = User.objects.get(id=user_id)
            training_count, created = TrainingCount.objects.get_or_create(user=client, label=label)
            training_count.count = F('count') + label_count
            training_count.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    