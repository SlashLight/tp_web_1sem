from django.shortcuts import render

# Create your views here.
QUESTIONS = [
    {
        "title": f"Question{i}",
        "id": f"{i}",
        "text": f"This is the question number {i}",
        "tags": f"tag{i % 2}"
    } for i in range(10)
]


def index(request):
    return render(request, 'index.html', {"questions": QUESTIONS})


def hot(request):
    return render(request, 'hot.html', {"questions": QUESTIONS[:5]})


def question(request, question_id):
    item = QUESTIONS[question_id]
    return render(request, 'question_detail.html', {"question": item})


def tag(request, tag_name):
    items = []
    for item in QUESTIONS:
        if item["tags"] == tag_name:
            items.append(item)
    return render(request, 'tag.html', {'questions': items, 'tag_name': tag_name})


def login(request):
    return render(request, 'login.html')


def signup(request):
    return render(request, 'signup.html')


def ask(request):
    return render(request, 'ask.html')


def settings(request):
    return render(request, 'settings.html')
