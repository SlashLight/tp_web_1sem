from django.core.paginator import Paginator
from django.shortcuts import render

# Create your views here.
QUESTIONS = [
    {
        "title": f"Question{i}",
        "id": i,
        "text": f"This is the question number {i}",
        "tags": f"tag{i % 2}"
    } for i in range(30)
]


def paginate(questions_list, request, per_page=5):
    paginator = Paginator(questions_list, per_page)
    page_num = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_num)
    return page_obj


def index(request):
    page_obj = paginate(QUESTIONS, request)
    return render(request, 'index.html', {"questions": page_obj})


def hot(request):
    page_obj = paginate(QUESTIONS[:15], request)
    return render(request, 'hot.html', {"questions": page_obj})


def question(request, question_id):
    item = QUESTIONS[question_id]
    return render(request, 'question_detail.html', {"question": item})


def tag(request, tag_name):
    items = []
    for item in QUESTIONS:
        if item["tags"] == tag_name:
            items.append(item)
    page_obj = paginate(items, request)
    return render(request, 'tag.html', {'questions': page_obj, 'tag_name': tag_name})


def login(request):
    return render(request, 'login.html')


def signup(request):
    return render(request, 'signup.html')


def ask(request):
    return render(request, 'ask.html')


def settings(request):
    return render(request, 'settings.html')
