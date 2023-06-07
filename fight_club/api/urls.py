from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views


app_name = 'api'

router = DefaultRouter()
router.register('calendar', views.TrainingViewSet, basename='calendar')

urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('calendar/label/', views.label_list, name='label_list'),
    path('calendar/today/', views.trainings_today, name='trainings_today'),
    path('calendar/this-week/', views.trainings_this_week, name='trainings_week'),
    path('calendar/this-month/', views.trainings_this_month, name='trainings_month'),
    path('users/trainers/', views.trainers_list, name='trainers_list'),
    path('users/admins/', views.admins_list, name='admins_list'),
    path('users/', views.UserList.as_view()),
    path('users/<int:pk>/', views.UserDetail.as_view()),
    path('users/profile/<int:pk>/', views.UserProfile.as_view()),
    path('tasks/', views.TaskListView.as_view(), name='task-list'),
    path('tasks/<int:pk>/', views.TaskDetailView.as_view(), name='task-detail'),
    path('tasks/past/', views.TaskPastView.as_view()),
    path('tasks/now/', views.TaskNowView.as_view()),
    path('tasks/future/', views.TaskFutureView.as_view()),
    path('tasks/count/', views.TaskCountView.as_view()),
    path('tasks/<int:pk>/comment/', views.CommentView.as_view()),
    path('payment/', views.PaymentView.as_view()),
    path('', include(router.urls)),
]
