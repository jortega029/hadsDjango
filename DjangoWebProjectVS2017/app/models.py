"""
Definition of models.
"""

from django.db import models
from django.db.models.fields import CharField

# Create your models here.
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

class Choice(models.Model):
    question = models.ForeignKey(Question)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

class User(models.Model):
    email = models.CharField(max_length=200)
    nombre = models.CharField(max_length=200)

class Pregunta(models.Model):
    texto = models.CharField(max_length=200)
    tema = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

class Respuesta(models.Model):
    pregunta = models.ForeignKey(Pregunta)
    isCorrect = models.BooleanField(default=False)
    textoRespuesta = models.CharField(max_length=200)
    votos = models.IntegerField(default=0)