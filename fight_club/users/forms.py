from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth import get_user_model
from .models import Profile


User = get_user_model()


#  создадим собственный класс для формы регистрации
#  сделаем его наследником предустановленного класса UserCreationForm
class CreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        # укажем модель, с которой связана создаваемая форма
        model = User
        # укажем, какие поля должны быть видны в форме и в каком порядке
        fields = ('full_name', 'email', 'phoneNumber',)


class ProfileForm(forms.ModelForm):
    class Meta:
        # На основе какой модели создаётся класс формы
        model = Profile
        # Укажем, какие поля будут в форме
        fields = ('gender', 'birthday', 'height', 'weight')