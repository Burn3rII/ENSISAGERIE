from django.db import models
from django.contrib.auth.models import User


class Room(models.Model):
    name = models.CharField(max_length=30)
    owner = models.ForeignKey(User, on_delete=models.CASCADE,)
    users = models.ManyToManyField(User, related_name="rooms")
    users_banned = models.ManyToManyField(User, related_name="banned_rooms",
                                          blank=True)
    private = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def pending_join_requests(self):
        return JoinRequest.objects.filter(room=self, is_approved=False)


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE,)
    room = models.ForeignKey(Room, on_delete=models.CASCADE,)
    publication_date = models.DateTimeField(auto_now_add=True)
    text = models.CharField(max_length=1000)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.text


class JoinRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.room.name}"


class RoomInvitation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.room.name}"
