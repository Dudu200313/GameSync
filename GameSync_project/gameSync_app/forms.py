from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Logview

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].error_messages.update({
            'unique': 'Este nome de usuário já está em uso.',
        })
        self.fields['password2'].error_messages.update({
            'password_mismatch': 'As senhas não coincidem.',
        })
        self.fields['email'].error_messages.update(
            {'valid' : 'Insira um email válido'}
        )

class LogviewForm(forms.ModelForm):
    class Meta:
        model = Logview
        fields = ['text', 'rating']
        widgets = {
            'rating': forms.Select(choices=[(x * 0.5, str(x * 0.5)) for x in range(1, 11)]),
            'text': forms.Textarea(attrs={'rows': 3}),
        }

