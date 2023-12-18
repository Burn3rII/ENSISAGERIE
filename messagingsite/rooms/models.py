from django.db import models
from django.contrib.auth.models import User


class Room(models.Model):
    name = models.CharField(max_length=150)
    owner = models.ForeignKey(User, on_delete=models.CASCADE,)
    users = models.ManyToManyField(User, related_name="rooms")

    def __str__(self):
        return self.name


class Message(models.Model):
    text = models.CharField(max_length=1000)
    sender = models.ForeignKey(User, on_delete=models.CASCADE,)
    room = models.ForeignKey(Room, on_delete=models.CASCADE,)
    publication_date = models.DateTimeField('date published')
