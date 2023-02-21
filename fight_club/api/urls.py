from django.urls import path
from . import views


app_name = 'api'

urlpatterns = [
    # Cтраница с задачами
    path('label/', views.label_list, name='label_list'),
]