from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse

from polls.models import Question


def index(request):
    qs = Question.objects.all()
    return render(request, 'index.html', {'questions': qs})

def detail(request, question_id):
    q = get_object_or_404(Question, pk=question_id)
    return render(request, 'detalle.html', {'question': q})

def vote(request, question_id):
    q = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = q.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return HttpResponse('Error')
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('index'))
