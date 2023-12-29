from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from django.template.loader import render_to_string
from .forms import RoomCreationForm
from .models import Room, Message
from django.shortcuts import render, get_object_or_404
"""from django.contrib.auth.models import User
from django.contrib.auth.models import Group"""


class RoomCreationView(CreateView):
    template_name = 'rooms/create.html'
    form_class = RoomCreationForm
    success_url = reverse_lazy('main:home')

    def form_valid(self, form):
        objet = form.save(commit=False)
        objet.owner = self.request.user
        objet.save()
        objet.users.add(self.request.user)

        return super().form_valid(form)


class RoomDetailView(TemplateView):
    template_name = 'rooms/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        room_id = kwargs['room_id']
        room = Room.objects.get(id=room_id)
        context['room'] = room

        return context


def search_rooms(request):
    if request.method == 'GET':
        search_term = request.GET.get('search_term', '')
        rooms = Room.objects.filter(name__icontains=search_term)[:5]
        search_results_html = render_to_string('rooms/search_results.html',
                                               {'search_results': rooms})

        return JsonResponse({'search_results_html': search_results_html})
    else:
        return JsonResponse({'error': 'Méthode non autorisée'})


def detail(request, room_id):
    room = get_object_or_404(Room, pk=room_id)
    return render(request, 'rooms/detail.html', {'room': room})


def send_message(request):
    if request.method == 'POST':
        room_id = request.POST.get('room_id')
        message_content = request.POST.get('message')
        room = get_object_or_404(Room, pk=room_id)
        sender = request.user

        # Save message to database
        Message.objects.create(room=room, sender=sender,
                               text=message_content)
        
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error'})

def message_number(request):
    if request.method == 'GET':
        room_id = request.GET.get('room_id')
        room = get_object_or_404(Room, pk=room_id)
        message_number = Message.objects.filter(room=room).count()
        
        return JsonResponse({'message_number': message_number})
    
    else:
        return JsonResponse({'status': 'error'})

def load_messages(request):
    if request.method == 'GET':
        room_id = request.GET.get('room_id')
        message_number = int(request.GET.get('message_number'))
        room = get_object_or_404(Room, pk=room_id)
        message_count = Message.objects.filter(room=room).count()
        messages = Message.objects.filter(room=room).order_by('-publication_date').reverse()[message_count-message_number:]

        return render(request, 'rooms/messages.html', {'messages': messages})
    else:
        return JsonResponse({'status': 'error'})
    
def load_all_messages(request):
    if request.method == 'GET':
        room_id = request.GET.get('room_id')
        room = get_object_or_404(Room, pk=room_id)
        messages = Message.objects.filter(room=room).order_by('-publication_date').reverse()

        return render(request, 'rooms/messages.html', {'messages': messages})
    else:
        return JsonResponse({'status': 'error'})







"""
def add_member(request, room_id, user_id):
    room = get_object_or_404(ChatRoom, pk=room_id)
    user = get_object_or_404(get_user_model(), pk=user_id)

    if request.user == room.owner:
        room.members.add(user)
        return HttpResponse("Member added successfully.")
    else:
        return HttpResponseForbidden("Permission denied. Only the owner can add members.")

def delete_chat_room(request, room_id):
    room = get_object_or_404(ChatRoom, pk=room_id)

    if request.user == room.owner:
        room.delete()
        return HttpResponse("Chat room deleted successfully.")
    else:
        return HttpResponseForbidden("Permission denied. Only the owner can delete the chat room.")

"""