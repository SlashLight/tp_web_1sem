from django.urls import path

from app import views

urlpatterns = [
    path('', views.index, name='index'),
    path('hot/', views.hot, name='index'),
    path('question/<int:question_id>', views.question, name='question'),
    path('tag/<str:tag_name>', views.tag, name='tag'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('ask/', views.ask, name='ask'),
    path('settings/', views.settings, name='settings')
]