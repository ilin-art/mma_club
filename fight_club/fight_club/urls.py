from django.contrib import admin
from django.urls import include, path

from .views import IndexView


app_name = 'fight_club'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('tasks/', include(('tasks.urls', 'tasks'), namespace='tasks')),
    path('calendar/', include(('training_calendar.urls', 'calendar'), namespace='calendar')),
    path('api/', include(('api.urls', 'api'), namespace='api')),
    path('admin/', admin.site.urls),
    path('auth/', include('users.urls')),
    path('auth/', include('django.contrib.auth.urls')),
]
