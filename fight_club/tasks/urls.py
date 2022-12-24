from django.urls import path
from . import views


app_name = 'tasks'

urlpatterns = [
    # Cтраница с задачами
    path('', views.tasks, name='tasks'),
] 