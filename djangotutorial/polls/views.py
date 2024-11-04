from django.shortcuts import render

# Create your views here.
# view는 일반적으로 특정한 기능을 제공하고 특정한 템플릿을 가진 Django 애플리케이션에 있는 웹페이지의 type이다.

# 각 뷰는 두 가지 중 하나를 하도록 되어 있다. 요청된 페이지의 내용이 담긴 HttpResponse 객체를 반환하거나, 
# 혹은 Http404같은 예외를 발생하게 해야한다.
# from django.http import Http404
from django.db.models import F
from django.http import HttpResponse, HttpResponseRedirect
# from django.template import loader
from django.shortcuts import get_object_or_404, render
# template에 context를 채워넣어 표현한 결과를 HttpResponse객체와 함께 돌려주는 구문은 자주 쓰는 용법이다.
# 따라서 Django는 이런 표현을 쉽게 표현할 수 있도록 단축 기능을 제공한다.

from django.urls import reverse

from .models import Choice, Question

def index(request):
  latest_question_list = Question.objects.order_by("-pub_date")[:5]
  # template = loader.get_template("polls/index.html")
  context = {
    "latest_question_list": latest_question_list,
  }
  return render(request, "polls/index.html", context)
  # return HttpResponse(template.render(context, request))

# def detail(request, question_id):
#     try:
#         question = Question.objects.get(pk=question_id)
#     except Question.DoesNotExist:
#         raise Http404("Question does not exist")
#     return render(request, "polls/detail.html", {"question": question})

def detail(request, question_id):
  question = get_object_or_404(Question, pk=question_id)
  return render(request, "polls/detail.html", {"question": question})

def results(request, question_id):
   question = get_object_or_404(Question, pk=question_id)
   return render(request, "polls/results.html", {"question":question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
    