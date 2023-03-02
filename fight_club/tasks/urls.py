from django.urls import path
from . import views


app_name = 'tasks'

urlpatterns = [
    path('', views.tasks, name='tasks'),
    path('<int:task_id>/comment/', views.add_comment, name='add_comment'),
]
