from django.contrib import admin
from django.urls import include, path


app_name = 'fight_club'

urlpatterns = [
    # path('', vies.index),
    path('tasks/', include(('tasks.urls', 'tasks'), namespace='tasks')),
    path('admin/', admin.site.urls),
    path('auth/', include('users.urls')),
    path('auth/', include('django.contrib.auth.urls')),
]
