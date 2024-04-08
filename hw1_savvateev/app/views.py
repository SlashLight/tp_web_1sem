from django.core.paginator import Paginator
from django.shortcuts import render

from app.models import Question, Answer


# Create your views here.


def paginate(questions_list, request, per_page=5):
    paginator = Paginator(questions_list, per_page)
    page_num = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_num)
    return page_obj


def index(request):
    questions = Question.objects.get_new_questions()
    page_obj = paginate(questions, request)
    return render(request, 'index.html', {"questions": page_obj})


def hot(request):
    questions = Question.objects.get_hot_questions()
    page_obj = paginate(questions, request)
    return render(request, 'hot.html', {"questions": page_obj})


def question(request, question_id):
    item = Question.objects.get_question_by_id(question_id)
    answers = Answer.objects.get_related_answers(question_id)
    return render(request, 'question_detail.html', {"question": item, "answers": answers})


def tag(request, tag_name):
    questions = Question.objects.get_questions_by_tag(tag_name)
    page_obj = paginate(questions, request)
    return render(request, 'tag.html', {'questions': page_obj, 'tag_name': tag_name})


def login(request):
    return render(request, 'login.html')


def signup(request):
    return render(request, 'signup.html')


def ask(request):
    return render(request, 'ask.html')


def settings(request):
    return render(request, 'settings.html')
