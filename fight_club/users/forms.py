from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth import get_user_model
from .models import Profile


User = get_user_model()


class CreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('full_name', 'email', 'phoneNumber',)


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('gender', 'birthday', 'height', 'weight')
