from django.shortcuts import render
from django.views.generic import View
from .scripts import authorized_only


class CalendarView(View):

    # @authorized_only
    def get(self, request, *args, **kwargs):
        return render(request, 'calendar/examples/example00-basic.html')
    