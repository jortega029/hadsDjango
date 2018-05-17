"""
Definition of forms.
"""

from django import forms
from app.models import Question,Choice,User,Pregunta,Respuesta
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _

class QuestionForm(forms.ModelForm):

        class Meta:
            model = Question
            fields = ('question_text',)

class ChoiceForm(forms.ModelForm):

        class Meta:
            model = Choice
            fields = ('choice_text',)

class UserForm(forms.ModelForm):

        class Meta:
            model = User
            fields = ('email','nombre',)

class AnadirForm(forms.ModelForm):

        class Meta:
            model = Pregunta
            fields = ('texto','tema',)

class RespuestasForm(forms.ModelForm):
        
        class Meta:
            model = Respuesta
            fields = ('textoRespuesta','isCorrect',)


class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'User name'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))
