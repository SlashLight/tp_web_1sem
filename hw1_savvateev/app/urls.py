from django.urls import path

from app import views

urlpatterns = [
    path('', views.index, name='index'),
    path('hot/', views.hot, name='hot'),
    path('question/<int:question_id>', views.question, name='question'),
    path('tag/<str:tag_name>', views.tag, name='tag'),
    path('login/', views.log_in, name='login'),
    path('signup/', views.sign_up, name='signup'),
    path('logout/', views.logout, name='logout'),
    path('ask/', views.ask, name='ask'),
    path('settings/', views.settings, name='settings'),
    path('<int:post_id>/like/', views.like, name='like'),
    path('<int:answer_id>/correct/', views.correct, name='correct'),
]
