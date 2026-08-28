from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
#secure version:
#from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
#vulnerable version:
from django.views.decorators.csrf import csrf_exempt
from django.db import connection

from .models import Choice, Question
from .forms import CreateUserForm


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        query = self.request.GET.get('q', '')

        if query:
            #secure version:
            #return Question.objects.filter(
                #question_text__icontains=query
                #)
            
            #vulnerable version:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT id FROM polls_question WHERE question_text LIKE '%"
                    + query +
                    "%'"
                )

                question_ids = [row[0] for row in cursor.fetchall()]

            return Question.objects.filter(id__in=question_ids)

        return Question.objects.order_by('-pub_date')[:5]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        return context


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

#secure version:
#@login_required
#vulnerable version:
@csrf_exempt
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
    
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


def register(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('polls:index')

    else:
        form = CreateUserForm()

    return render(request, 'polls/register.html', {'form': form})


