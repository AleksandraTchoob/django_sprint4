from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()


class CreationForm(UserCreationForm):
    """Форма для регистрации пользователей."""
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name', 'last_name', 'username', 'email')


class ProfileEditForm(forms.ModelForm):
    """Форма для редактирования профиля."""
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email')
