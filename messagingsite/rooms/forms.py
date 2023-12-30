from django.forms import ModelForm
from .models import Room


class RoomCreationForm(ModelForm):
    class Meta:
        model = Room
        fields = ["name", "private"]
        labels = {
            "name": "Nom du salon",
            "private": "Rendre le salon privé (les utilisateurs souhaitant "
                       "accéder au salon devront d'abord en faire la demande)"
        }
