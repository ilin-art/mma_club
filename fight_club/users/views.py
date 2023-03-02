from django.views.generic import CreateView, View, FormView

# Функция reverse_lazy позволяет получить URL по параметрам функции path()
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect

from .forms import CreationForm, ProfileForm
from tasks.forms import TaskForm
from .models import User, Profile
from tasks.models import Task
from .scripts import authorized_only


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('users:login')
    template_name = 'users/signup.html'

@method_decorator(authorized_only, name='dispatch')
class ProfileView(View):
    template_name = 'users/profile.html'

    def get(self, request, username, *args, **kwargs):
        user = get_object_or_404(User, phoneNumber=username)
        name = user.full_name
        email = user.email
        phoneNumber = user.phoneNumber
        registration_date = user.registration_date
        last_login = user.last_login
        profile = get_object_or_404(Profile, user=user)
        task = get_object_or_404(Task, user=user)

        global context

        context = {
        'name': name,
        'email': email,
        'phoneNumber': phoneNumber,
        'registration_date': registration_date,
        'last_login': last_login,
        }

        profile_form = ProfileForm(self.request.GET or None, instance=profile)
        task_form = TaskForm(self.request.GET or None, instance=task)
        context['profile_form'] = profile_form
        context['task_form'] = task_form
        return render(request, 'users/profile.html', context)
     
    def post(self, request, username, *args, **kwargs):
        user = get_object_or_404(User, phoneNumber=username)
        profile = get_object_or_404(Profile, user=user)
        task = get_object_or_404(Task, user=user)
        profile_form = ProfileForm(
            request.POST or None,
            request.FILES or None,
            instance=profile
        )
        task_form = TaskForm(
            request.POST or None,
            request.FILES or None,
            instance=task
        )
        if task_form.is_valid():
            task_form.save()
        if profile_form.is_valid():
            profile_form.save()
            return redirect(request.META.get('HTTP_REFERER','redirect_if_referer_not_found'))
        return render(request, 'users/profile.html', context)


class ProfileFormView(FormView):
    form_class = ProfileForm
    template_name = 'users/profile.html'
    success_url = '/tasks'

    def post(self, request, username, *args, **kwargs):
        profile_form = self.form_class(request.POST or None)
        if profile_form.is_valid():
            profile_form.save()
            return self.render_to_response(
                self.get_context_data(
                success=True
            )
        )
        else:
            return self.render_to_response(
            self.get_context_data(
                    profile_form=profile_form,
            )
        )
# Перенапарвление в профиль user после логина
@authorized_only
def profile(request):
    url = '%s/' % request.user.phoneNumber
    return HttpResponseRedirect(url)

@authorized_only
def users_list(request):
    users = User.objects.order_by('-registration_date')
    context = {
        'users': users,
    }
    return render(request, 'users/users.html', context)
