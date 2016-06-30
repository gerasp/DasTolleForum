from django.db import models
from django.contrib.auth.models import User, Group

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    photo = models.ImageField(upload_to='profiles',default='profiles/default.jpg')
    no_of_messages = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username

class Topic(models.Model):
    name = models.CharField(max_length=30)
    no_of_threads = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class Thread(models.Model):
    title = models.CharField(max_length=100)
    topic = models.ForeignKey(Topic) #1:N
    no_of_messages = models.IntegerField(default=0)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Message(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField(max_length=1000)
    date_created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(UserProfile) #1:N
    thread = models.ForeignKey(Thread) #1:N

    def __str__(self):
        return self.title