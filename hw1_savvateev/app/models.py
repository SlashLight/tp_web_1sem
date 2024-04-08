from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class QuestionManager(models.Manager):
    def get_new_questions(self):
        return self.order_by('-created_at')

    def get_question_by_id(self, question_id):
        return self.get(id=question_id)

    def get_hot_questions(self):
        return self.order_by('-content__likes')

    def get_questions_by_tag(self, tag):
        return self.filter(tags__name__icontains=tag)


class AnswerManager(models.Manager):
    def get_related_answers(self, question_id):
        return self.filter(related_question__id=question_id)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    avatar = models.ImageField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username


class Post(models.Model):
    content = models.TextField(max_length=500)
    likes = models.IntegerField(default=0)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content[:20]


class Tag(models.Model):
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Question(models.Model):
    content = models.ForeignKey(Post, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    tags = models.ManyToManyField(Tag, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = QuestionManager()

    def __str__(self):
        return self.title


class Answer(models.Model):
    CORRECT_CHOICES = (('checked', 'checked'), ('', 'not'))
    content = models.ForeignKey(Post, on_delete=models.CASCADE)
    related_question = models.ForeignKey(Question, on_delete=models.CASCADE)
    correct = models.CharField(choices=CORRECT_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = AnswerManager()


class Like(models.Model):
    LIKE_CHOICES = ((1, 'Like'), (2, 'Dislike'))
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    user_id = models.ForeignKey(Profile, on_delete=models.CASCADE)
    like = models.CharField(max_length=1, choices=LIKE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
