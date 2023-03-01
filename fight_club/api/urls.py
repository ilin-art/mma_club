from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views


app_name = 'api'

router = DefaultRouter()
router.register('trainings', views.TrainingViewSet)
# router.register('trainings-name', views.TrainingNameViewSet) 

urlpatterns = [
    # Cтраница с задачами
    path('calendar/label/', views.label_list, name='label_list'),
    path('calendar/', include(router.urls)),
    path('calendar/trainings-name/', views.trainings_list_name, name='trainings_list_name'),
    path('users/trainers/', views.trainers_list, name='trainers_list'),
    path('users/admins/', views.admins_list, name='admins_list'),
    path('users/', views.users_list, name='users_list'),
]