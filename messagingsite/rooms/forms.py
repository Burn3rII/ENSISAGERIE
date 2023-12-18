from django.forms import ModelForm
from .models import Room


class RoomCreationForm(ModelForm):
    class Meta:
        model = Room
        fields = ["name"]
        labels = {
            "name": "Nom du salon",
        }
