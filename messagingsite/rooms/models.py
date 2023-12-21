from django.db import models
from django.contrib.auth.models import User


class Room(models.Model):
    name = models.CharField(max_length=30)
    owner = models.ForeignKey(User, on_delete=models.CASCADE,)
    users = models.ManyToManyField(User, related_name="rooms")

    def __str__(self):
        return self.name


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE,)
    room = models.ForeignKey(Room, on_delete=models.CASCADE,)
    publication_date = models.DateTimeField(auto_now_add=True)
    text = models.CharField(max_length=1000)

