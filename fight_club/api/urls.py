from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views


app_name = 'api'

router = DefaultRouter()
router.register('calendar', views.TrainingViewSet, basename='calendar')

urlpatterns = [
    # Cтраница с задачами
    path('calendar/label/', views.label_list, name='label_list'),
    path('', include(router.urls)),
    # path('calendar/', views.trainings_list, name='trainings_list'),
    # path('calendar/<int:pk>/', views.trainings_detail, name='trainings_detail_name'),
    path('calendar/today/', views.trainings_today, name='trainings_today'),
    path('calendar/this-week/', views.trainings_this_week, name='trainings_week'),
    path('calendar/this-month/', views.trainings_this_month, name='trainings_month'),
    # path('calendar/filter/', views.trainings_filter, name='trainings-filter'),
    path('users/trainers/', views.trainers_list, name='trainers_list'),
    path('users/admins/', views.admins_list, name='admins_list'),
    path('users/', views.users_list, name='users_list'),
]
