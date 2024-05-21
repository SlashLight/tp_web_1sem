from django.contrib import auth
from django.contrib.auth import authenticate, login
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.db.models import Count
from django.http import JsonResponse

from app.forms import LoginForm, RegisterForm, QuestionForm, answerForm
from app.models import Question, Answer, Tag, Post, Like

from app.forms import ProfileForm
from app.models import Profile


# Create your views here.


def paginate(questions_list, request, per_page=5):
    paginator = Paginator(questions_list, per_page)
    page_num = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_num)
    return page_obj


popular_tags = Tag.objects.annotate(t_count=Count('question')).order_by('-t_count')[:8]


def index(request):
    user = Profile.objects.get(user=request.user)
    questions = Question.objects.get_new_questions()
    page_obj = paginate(questions, request)
    return render(request, 'index.html', {"questions": page_obj, "author": user, "popular_tags": popular_tags})


def hot(request):
    user = Profile.objects.get(user=request.user)
    questions = Question.objects.get_hot_questions()
    page_obj = paginate(questions, request)
    return render(request, 'hot.html', {"questions": page_obj, "author": user, "popular_tags": popular_tags})


def question(request, question_id):
    user = Profile.objects.get(user=request.user)
    item = Question.objects.get_question_by_id(question_id)
    answers = Answer.objects.get_related_answers(question_id)
    page_obj = paginate(answers, request)
    if request.method == 'GET':
        answer_form = answerForm()
    if request.method == 'POST':
        answer_form = answerForm(request.POST, user=request.user, question=item)
        if answer_form.is_valid():
            answer = answer_form.save()
            if answer:
                return redirect('question', question_id=item.id)
            else:
                answer_form.add_error(None, 'Error adding answer')
    return render(request, 'question_detail.html', {"question": item, "answers": page_obj, 'form': answer_form,
                                                    "author": user, "popular_tags": popular_tags})


def tag(request, tag_name):
    user = Profile.objects.get(user=request.user)
    questions = Question.objects.get_questions_by_tag(tag_name)
    page_obj = paginate(questions, request)
    return render(request, 'tag.html',
                  {'questions': page_obj, 'tag_name': tag_name, "author": user, "popular_tags": popular_tags})


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
    return render(request, 'login.html', context={'form': login_form, "popular_tags": popular_tags})


def sign_up(request):
    if request.method == 'GET':
        register_form = RegisterForm()
    if request.method == 'POST':
        register_form = RegisterForm(data=request.POST, files=request.POST)
        if register_form.is_valid():
            user = register_form.save()
            if user:
                return redirect(reverse('index'))
            else:
                register_form.add_error(field=None, error='Error saving user')
    return render(request, 'signup.html', context={'form': register_form, "popular_tags": popular_tags})


def logout(request):
    auth.logout(request)
    return redirect(reverse('login'))


def ask(request):
    user = Profile.objects.get(user=request.user)
    if request.method == 'GET':
        ask_form = QuestionForm()
    if request.method == 'POST':
        ask_form = QuestionForm(data=request.POST, request=request)
        if ask_form.is_valid():
            question = ask_form.save()
            if question:
                return redirect(reverse('question', args=[question.id]))
            else:
                ask_form.add_error(field=None, error='Error saving question')
    return render(request, 'ask.html', context={'form': ask_form, "author": user, "popular_tags": popular_tags})


def settings(request):
    user = Profile.objects.get(user=request.user)
    profile = Profile.profiles.get_by_username(request.user.username)
    if request.method == 'GET':
        settingsForm = ProfileForm(initial={
            'login': profile.user.username,
            'email': profile.user.email,
            'nickname': profile.nickname,
            'avatar': profile.avatar,
        })
    if request.method == 'POST':
        settingsForm = ProfileForm(data=request.POST, files=request.FILES, request=request)
        if settingsForm.is_valid():
            user = settingsForm.save()
            if user:
                return redirect(reverse('index'))
            else:
                settingsForm.add_error(field=None, error='Error saving user')
    return render(request, 'settings.html', context={'form': settingsForm, "author": user,
                                                     "popular_tags": popular_tags})


def like(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    profile = Profile.objects.get(user=request.user)
    post_like, post_like_created = Like.objects.get_or_create(post_id=post_id, user_id=profile.id, like=1)

    if not post_like_created:
        post_like.delete()

    return JsonResponse({'likes_count': post.likes})
