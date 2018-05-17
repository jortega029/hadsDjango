"""
Definition of views.
"""

from django.shortcuts import render,get_object_or_404
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from django.http.response import HttpResponse, Http404
from django.http import HttpResponseRedirect, HttpResponse
from .models import Question,Choice,User,Pregunta,Respuesta
from django.template import loader
from django.core.urlresolvers import reverse
from app.forms import QuestionForm, ChoiceForm,UserForm,AnadirForm,RespuestasForm
from django.shortcuts import redirect
import json


def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Home Page',
            'year':datetime.now().year,
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Autor de la web',
            'message':'Datos de contacto',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        }
    )
def index(request):
    latest_question_list = Pregunta.objects.order_by('-pub_date')
    preguntas = []
    listaTemas = []
    for preg in latest_question_list:
        if preg.tema not in listaTemas:
            listaTemas.append(preg.tema)
    if request.method == 'POST':
        tema = request.POST['temas']
        preguntas = filter(lambda preg: preg.tema == tema, latest_question_list)
        context = {
                'title':'Lista de preguntas de la encuesta',
                'latest_question_list': preguntas,
                'listaTemas' : listaTemas
              }
    else: 
        preguntas = latest_question_list
        template = loader.get_template('polls/index.html')
        context = {
                'title':'Lista de preguntas de la encuesta',
                'latest_question_list': preguntas,
                'listaTemas' : listaTemas
              }
    return render(request, 'polls/index.html', context)

def detail(request, question_id):
     question = get_object_or_404(Pregunta, pk=question_id)
     return render(request, 'polls/detail.html', {'title':'Respuestas asociadas a la pregunta:','question': question})

def results(request, question_id,idRespuesta):
    question = get_object_or_404(Pregunta, pk=question_id)
    respuesta = get_object_or_404(Respuesta, pk=idRespuesta)
    if respuesta.isCorrect:
        return render(request, 'polls/results.html', {'title':'Resultados de la pregunta:','question': question,'message':'Has acertado!!'})
    else:
        return render(request, 'polls/results.html', {'title':'Resultados de la pregunta:','question': question,'message':'Has fallado!!'})
    

def vote(request, question_id):
    p = get_object_or_404(Pregunta, pk=question_id)
    try:
        selected_choice = p.respuesta_set.get(pk=request.POST['respuesta'])
    except (KeyError, Respuesta.DoesNotExist):
        # Vuelve a mostrar el form.
        return render(request, 'polls/detail.html', {
            'question': p,
            'error_message': "ERROR: No se ha seleccionado una opcion",
        })
    else:
        selected_choice.votos += 1
        selected_choice.save()
        # Siempre devolver un HttpResponseRedirect despues de procesar
        # exitosamente el POST de un form. Esto evita que los datos se
        # puedan postear dos veces si el usuario vuelve atras en su browser.
        return HttpResponseRedirect(reverse('results', args=(p.id,selected_choice.id,)))

def question_new(request):
        if request.method == "POST":
            form = AnadirForm(request.POST)
            if form.is_valid():
                question = form.save(commit=False)
                question.pub_date=datetime.now()
                question.save()
                #return redirect('detail', pk=question_id)
                #return render(request, 'polls/choice_new.html', {'title':'Respuestas posibles','question': question})
        else:
            form = AnadirForm()

        return render(request, 'polls/question_new.html', {'title':'Añadir nueva pregunta','form': form})

def choice_add(request, question_id):
        question = Pregunta.objects.get(id = question_id)
        form = RespuestasForm()
        hayCorrecta = False
        for i in question.respuesta_set.all():
            if i.isCorrect:
                hayCorrecta = True
        if question.respuesta_set.count() == 4:
            return render(request, 'polls/choice_new.html', {'title':'Pregunta:'+ question.texto,'form': form,'mensaje':'Ya se han registrado 4 respuestas para esta pregunta'})
        else:
            if request.method =='POST':
                if hayCorrecta:
                    if correctaSeleccionado(request):
                        return render(request, 'polls/choice_new.html', {'title':'Pregunta:'+ question.texto,'form': form,'mensaje':'Esta pregunta ya tiene una correcta, no puedes poner más'})
                    else:
                        form = RespuestasForm(request.POST)
                        if form.is_valid():
                            choice = form.save(commit = False)
                            choice.pregunta = question
                            choice.votos = 0
                            choice.save()
                            #form.save()
                else:
                    form = RespuestasForm(request.POST)
                    if form.is_valid():
                        choice = form.save(commit = False)
                        choice.pregunta = question
                        choice.votos = 0
                        choice.save()
                        #form.save()
            return render(request, 'polls/choice_new.html', {'title':'Pregunta:'+ question.texto,'form': form})


def correctaSeleccionado(request):
    try:
        selected = request.POST["isCorrect"]
        seleccionado = True
        return seleccionado
    except:
        seleccionado = False
        return seleccionado


def chart(request, question_id):
    q=Pregunta.objects.get(id = question_id)
    qs = Respuesta.objects.filter(pregunta=q)
    dates = [obj.textoRespuesta for obj in qs]
    counts = [obj.votos for obj in qs]
    context = {
        'dates': json.dumps(dates),
        'counts': json.dumps(counts),
    }

    return render(request, 'polls/grafico.html', context)

def user_new(request):
        if request.method == "POST":
            form = UserForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.save()
                #return redirect('detail', pk=question_id)
                #return render(request, 'polls/index.html', {'title':'Respuestas posibles','question': question})
        else:
            form = UserForm()
        return render(request, 'polls/user_new.html', {'form': form})

def users_detail(request):
    latest_user_list = User.objects.order_by('email')
    template = loader.get_template('polls/users.html')
    context = {
                'title':'Lista de usuarios',
                'latest_user_list': latest_user_list,
              }
    return render(request, 'polls/users.html', context)