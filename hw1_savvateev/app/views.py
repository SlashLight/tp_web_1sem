from django.contrib import auth
from django.contrib.auth import authenticate, login
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from app.forms import LoginForm, RegisterForm
from app.models import Question, Answer

from app.forms import ProfileForm
from app.models import Profile


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
    page_obj = paginate(answers, request)
    return render(request, 'question_detail.html', {"question": item, "answers": page_obj})


def tag(request, tag_name):
    questions = Question.objects.get_questions_by_tag(tag_name)
    page_obj = paginate(questions, request)
    return render(request, 'tag.html', {'questions': page_obj, 'tag_name': tag_name})


@require_http_methods(["GET", "POST"])
def log_in(request):
    if request.method == 'GET':
        login_form = LoginForm()
    if request.method == 'POST':
        login_form = LoginForm(data=request.POST)
        if login_form.is_valid():
            user = authenticate(request, **login_form.cleaned_data)
            if user and user.is_active:
                login(request, user)
                return redirect(reverse('index'))
    return render(request, 'login.html', context={'form': login_form})


def sign_up(request):
    if request.method == 'GET':
        register_form = RegisterForm()
    if request.method == 'POST':
        register_form = RegisterForm(data=request.POST)
        if register_form.is_valid():
            user = register_form.save()
            if user:
                return redirect(reverse('index'))
            else:
                register_form.add_error(field=None, error='Error saving user')
    return render(request, 'signup.html', context={'form': register_form})


def logout(request):
    auth.logout(request)
    return redirect(reverse('login'))


def ask(request):
    return render(request, 'ask.html')


def settings(request):
    profile = Profile.profiles.get_by_username(request.user.username)
    if request.method == 'GET':
        settingsForm = ProfileForm( initial={
            'login': profile.user.username,
            'email': profile.user.email,
            'nickname': profile.nickname,
            'avatar': profile.avatar,
        })
    if request.method == 'POST':
        settingsForm = ProfileForm(data=request.POST, request=request)
        if settingsForm.is_valid():
            user = settingsForm.save()
            if user:
                return redirect(reverse('index'))
            else:
                settingsForm.add_error(field=None, error='Error saving user')
    return render(request, 'settings.html', context={'form': settingsForm})
