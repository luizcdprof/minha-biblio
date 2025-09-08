from django import forms
from django.contrib.auth.models import User
from django.db import transaction
from .models import Usuario, Turma

class UsuarioForm(forms.ModelForm):
    first_name = forms.CharField(label="Nome", max_length=150)
    last_name = forms.CharField(label="Sobrenome", max_length=150)
    email = forms.EmailField(label="E-mail")
    password = forms.CharField(label="Senha", widget=forms.PasswordInput, required=False)
    perfil = forms.ChoiceField(
        choices=Usuario.PERFIL_CHOICES,
        label="Perfil",
        required=True
    )

    class Meta:
        model = Usuario
        fields = ['imagem', 'ra', 'turma', 'telefone', 'perfil']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            # Inicializa campos do User
            user = self.instance.user
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
            self.fields['email'].initial = user.email
            self.fields['perfil'].initial = self.instance.perfil

    def save(self, commit=True):
        with transaction.atomic():
            if self.instance and self.instance.pk:
                user = self.instance.user
                user.first_name = self.cleaned_data['first_name']
                user.last_name = self.cleaned_data['last_name']
                user.email = self.cleaned_data['email']
                if self.cleaned_data['password']:
                    user.set_password(self.cleaned_data['password'])
                user.save()
                usuario = super().save(commit=False)
                usuario.user = user
                if commit:
                    usuario.save()
                return usuario
            else:
                user = User.objects.create_user(
                    username=self.cleaned_data['email'],
                    email=self.cleaned_data['email'],
                    password=self.cleaned_data['password'],
                    first_name=self.cleaned_data['first_name'],
                    last_name=self.cleaned_data['last_name'],
                )
                usuario = super().save(commit=False)
                usuario.user = user
                if commit:
                    usuario.save()
                return usuario

class TurmaForm(forms.ModelForm):
    class Meta:
        model = Turma
        fields = ['nome', 'periodo']

class LoginForm(forms.Form):
    email = forms.EmailField(label="E-mail", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="Senha", widget=forms.PasswordInput(attrs={'class': 'form-control'}))