from django.db import models
from django.contrib.auth import models as models_auth
from django.urls import reverse

# Create your models here.

class Reaction():
    def __init__(self):
        pass

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()


class Author(models.Model):
    rating = models.IntegerField(default=0)
    user = models.OneToOneField(models_auth.User, on_delete=models.CASCADE)

    def update_rating(self):
        posts_rating = 0
        comments_rating = 0
        posts_comment_rating = 0

        posts = Post.objects.filter(author=self)
        for post in posts:
            posts_rating += post.rating

        comments = Comment.objects.filter(user=self.user)
        for comment in comments:
            comments_rating += comment.rating

        posts_comments = Comment.objects.filter(post__author=self)
        for post_comment in posts_comments:
            posts_comment_rating += post_comment.rating

        self.rating = posts_rating * 3 + comments_rating + posts_comment_rating
        self.save()

class Category(models.Model):
    name = models.CharField(unique=True, max_length=100)
    subscribers = models.ManyToManyField(models_auth.User, related_name='categories')


class Post(models.Model, Reaction):
    article = 'AR'
    news = 'NW'
    TYPES = [
        (article, 'article'),
        (news, 'news')
    ]

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    category = models.ManyToManyField(Category, through='PostCategory')
    type = models.CharField(choices=TYPES, default=news, max_length=2)
    date_time = models.DateTimeField(auto_now_add=True)
    subject = models.CharField(max_length=100)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    def preview(self):
        return f"{self.text[:124]}..."

    def __str__(self):
        return f"{self.text}"

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])


class PostCategory(models.Model):
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model, Reaction):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(models_auth.User, on_delete=models.CASCADE)
    text = models.TextField()
    date_time = models.DateField(auto_now_add=True)
    rating = models.IntegerField(default=0)

