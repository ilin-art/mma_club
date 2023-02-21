from rest_framework.decorators import api_view  # Импортировали декоратор
from rest_framework.response import Response  # Импортировали класс Response
from rest_framework import status

from .serializers import LabelSerializer

from training_calendar.models import Label

@api_view(['GET', 'POST'])  # Разрешены только POST- и GET-запросы
def label_list(request):
    # В случае POST-запроса добавим список записей в БД
    if request.method == 'POST':
        serializer = LabelSerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # В случае GET-запроса возвращаем список всех котиков
    labels = Label.objects.all()
    serializer = LabelSerializer(labels, many=True)
    return Response(serializer.data) 
