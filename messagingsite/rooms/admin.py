from django.contrib import admin
from .models import Room, Message, JoinRequest, RoomInvitation

admin.site.register(Room)
admin.site.register(Message)
admin.site.register(JoinRequest)
admin.site.register(RoomInvitation)

