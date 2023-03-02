from .views import CalendarView
from django.urls import path

app_name = 'calendar'

urlpatterns = [
    path(
      '',
      CalendarView.as_view(),
      name='calendar_main'
    ),
]
