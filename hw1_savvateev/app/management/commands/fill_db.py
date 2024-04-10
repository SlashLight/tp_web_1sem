import random

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError

from app.models import Profile, Question, Post, Tag, Answer, Like


class Command(BaseCommand):
    help = "Closes the specified poll for voting"

    def add_arguments(self, parser):
        parser.add_argument(action="store", type=int, dest="ratio")

    def handle(self, *args, **options):
        ratio = options["ratio"]
        profiles = []
        users = []
        for i in range(ratio):
            user = User(
                username=f"user{i}",
                password="<PASSWORD>"
            )
            users.append(user)
            profiles.append(Profile(user=user))
        User.objects.bulk_create(users)
        Profile.objects.bulk_create(profiles)

        tags = []
        for i in range(ratio):
            tag = Tag(
                name=f"tag{i}"
            )
            tags.append(tag)
        Tag.objects.bulk_create(tags)

        questions = []
        posts = []
        for i in range(ratio * 10):
            author = profiles[random.randint(1, ratio - 1)]
            post = Post(
                content=f"Fish{i} --- Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent semper lobortis ipsum, et interdum sem lobortis et",
                author=author
            )
            posts.append(post)
            question = Question(
                content=post,
                title=f"question number {i}",
            )
            questions.append(question)
        Post.objects.bulk_create(posts)
        Question.objects.bulk_create(questions)

        for i in range(ratio * 10):
            question = questions[i]
            question.tags.add(tags[random.randint(1, ratio - 1)])

        apost = []
        answers = []
        for i in range(ratio * 100):
            author = profiles[random.randint(1, ratio - 1)]
            post = Post(
                content=f"Fish{i} --- Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent semper lobortis ipsum, et interdum sem lobortis et",
                author=author
            )
            apost.append(post)
            answer = Answer(
                content=post,
                related_question=questions[random.randint(0, ratio * 10 - 1)]
            )
            answers.append(answer)
        Post.objects.bulk_create(apost)
        Answer.objects.bulk_create(answers)
        posts.extend(apost)
        likes = []
        for i in range(ratio * 200):
            post_id = random.randint(1, len(posts) - 1)
            post = posts[post_id]
            author = profiles[random.randint(1, ratio - 1)]
            like = Like(
                post_id=post,
                user_id=author
            )
            likes.append(like)
            posts[post_id].likes += 1
        Like.objects.bulk_create(likes)
        Post.objects.bulk_update(posts, ['likes'])

