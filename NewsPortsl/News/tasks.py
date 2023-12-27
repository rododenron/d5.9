from datetime import datetime, timedelta

from celery import shared_task
import time

from django.core.mail import send_mail

from .models import Category, Post
from NewsPortsl import settings

@shared_task
def send_message():
    for cat in Category.objects.all():
        for subscriber in cat.subscribers.all():
            send_mail(
                "Created news!",
                "New text.",
                settings.DEFAULT_FROM_EMAIL,
                recipient_list=[subscriber]
            )

@shared_task
def send_message_news():
    posts = Post.objects.filter(date_time__gt=(datetime.now() - timedelta(days=7)))

    message = ""
    for post in posts:
        message += f"News: {post.subject}\n\r"
    if message:
        for cat in Category.objects.all():
            for subscriber in cat.subscribers.all():
                send_mail(
                    "Created news for last week!",
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[subscriber]
                )