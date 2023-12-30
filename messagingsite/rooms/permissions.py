from django.contrib.auth.models import Permission

chatroom_add_member = Permission.objects.create(
    codename='chatroom_add_member',
    name="Permet d'ajouter un membre au salon",
)

chatroom_delete = Permission.objects.create(
    codename='chatroom_delete',
    name='Permet de supprimer un membre au salon',
)
