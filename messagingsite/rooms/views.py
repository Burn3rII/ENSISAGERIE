import os
import json
from django.templatetags.static import static
from django.views.generic.edit import CreateView
from django.db.models import Q
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.template.loader import render_to_string
from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET, require_POST

from django.contrib.auth.models import User
from .models import Room, Message, JoinRequest, RoomInvitation

from .forms import RoomCreationForm

"""from django.contrib.auth.models import User
from django.contrib.auth.models import Group"""


# Sur la page d'accueil--------------------------------------------------------
@login_required  # Si le user n'est pas connecté, redirige vers la page de
# connexion
def detail(request, room_id):
    room = get_object_or_404(Room, pk=room_id)

    if request.user not in room.users.all():  # Condition : le user actuel
        # doit faire partie du salon.
        return render(request, 'main/403.html', status=403)

    context = {'room': room}
    return render(request, 'rooms/detail.html', context)


@login_required
@require_POST
def accept_invitation(request):
    invitation_id = request.POST.get('invitation_id', '')
    invitation = get_object_or_404(RoomInvitation, id=invitation_id)

    if invitation.user != request.user:  # Condition : l'invitation doit
        # être adressée au user actuel
        return render(request, 'main/403.html', status=403)

    invitation.room.users.add(invitation.user)
    invitation.delete()

    return JsonResponse({'message': "L'invitation a été acceptée."})


@login_required
@require_POST
def reject_invitation(request):
    invitation_id = request.POST.get('invitation_id', '')
    invitation = get_object_or_404(RoomInvitation, id=invitation_id)

    if invitation.user != request.user:  # Condition : l'invitation doit
        # être adressée au user actuel
        return render(request, 'main/403.html', status=403)

    invitation.delete()

    return JsonResponse({'message': "L'invitation a été refusée."})


@login_required
@require_POST
def delete_accepted_request(request):
    request_id = request.POST.get('request_id', '')
    accepted_request = get_object_or_404(JoinRequest, id=request_id)

    if accepted_request.user != request.user:  # Condition : la requête doit
        # avoir été créée par le user actuel
        return render(request, 'main/403.html', status=403)

    accepted_request.delete()

    return JsonResponse({'message': "La demande a été détruite."})


@login_required
@require_GET
def search_room(request):
    search_term = request.GET.get('search_term', '')
    user = request.user
    rooms = Room.objects.filter(
        Q(name__icontains=search_term) &
        ~Q(users=user) &
        ~Q(joinrequest__user=user, joinrequest__is_approved=False)
    )[:5]  # Q crée une condition de requête et ~Q crée la négation (NOT)
    # d'une condition de requête.
    search_results_html = render_to_string(
        'rooms/rooms_search_results.html', {'search_results': rooms})

    return JsonResponse({'rooms_search_results_html': search_results_html})


@login_required
@require_POST
def join_room(request):
    room_id = request.POST.get('room_id', '')
    room = get_object_or_404(Room, id=room_id)

    if not room.private:
        room.users.add(request.user)

        return JsonResponse(
            {'message': 'Vous avez rejoint le salon avec succès!'})


@login_required
@require_POST
def request_to_join(request):
    room_id = request.POST.get('room_id', '')
    room = get_object_or_404(Room, id=room_id, private=True)

    if room.private:
        join_request = JoinRequest(user=request.user, room=room)
        join_request.save()

        return JsonResponse({'message': 'Votre demande a été envoyée au '
                                        'propriétaire du salon.'})


# Sur la page de création de salon---------------------------------------------
@method_decorator(login_required, name='dispatch')
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


# Sur une page de salon--------------------------------------------------------
@login_required
def user_management(request, room_id):
    room = get_object_or_404(Room, pk=room_id)

    if room.owner != request.user:  # Condition : le user actuel doit être
        # le propriétaire du salon.
        return render(request, 'main/403.html', status=403)

    context = {'room': room}

    return render(request, 'rooms/user_management.html', context)


@login_required
@require_POST
def send_message(request):
    room_id = request.POST.get('room_id')
    room = get_object_or_404(Room, pk=room_id)
    message_content = request.POST.get('message')

    Message.objects.create(room=room, sender=request.user,
                           text=message_content)

    return JsonResponse({'message': 'Le message a été envoyé.'})


@login_required
@require_GET
def get_message_number(request):
    room_id = request.GET.get('room_id')
    room = get_object_or_404(Room, pk=room_id)
    message_number = Message.objects.filter(room=room).count()

    return JsonResponse({'message_number': message_number})


@login_required
@require_GET
def load_messages(request):
    room_id = request.GET.get('room_id')
    room = get_object_or_404(Room, pk=room_id)
    message_number = int(request.GET.get('message_number'))
    message_count = Message.objects.filter(room=room).count()
    messages = Message.objects.filter(room=room).order_by(
        '-publication_date').reverse()[message_count - message_number:]

    return render(request, 'rooms/messages.html', {'messages': messages})


@login_required
@require_GET
def load_all_messages(request):
    room_id = request.GET.get('room_id')
    room = get_object_or_404(Room, pk=room_id)
    messages = Message.objects.filter(room=room).order_by(
        '-publication_date').reverse()

    return render(request, 'rooms/messages.html', {'messages': messages})


@login_required
def emoji_list(request):
    json_file_path = os.path.join(static('rooms/json'), 'data_by_groups.json')

    with open(json_file_path, 'r', encoding='utf-8') as file:
        emoji_data = json.load(file)

    # Convert emoji data to a JSON-compatible format
    emoji_data_json = {category: [{'char': emoji['char'],
                                   'name': emoji['name']} for emoji in emojis]
                       for category, emojis in emoji_data.items()}

    return JsonResponse(emoji_data_json, safe=False)


# Sur une page de gestion des utilisateurs d'un salon--------------------------
@login_required
@require_GET
def search_invite_user(request):
    search_term = request.GET.get('search_term', '')
    room_id = request.GET.get('room_id', '')
    room = get_object_or_404(Room, pk=room_id)

    if room.owner != request.user:  # Condition : le user actuel doit être
        # le propriétaire du salon.
        return render(request, 'main/403.html', status=403)

    room_users = User.objects.filter(
        Q(username__icontains=search_term) &
        ~Q(rooms__id=room_id) &
        ~Q(roominvitation__room_id=room_id))[:5]  # Q crée une condition
    # de requête et ~Q crée la négation (NOT) d'une condition de requête.
    search_results_html = render_to_string(
        'rooms/invite_users_search_results.html',
        {'room_id': room_id, 'search_results': room_users})

    return JsonResponse({'invite_users_search_results_html': search_results_html})


@login_required
@require_POST
def invite(request):
    room_id = request.POST.get('room_id', '')
    user_id = request.POST.get('user_id', '')
    room = get_object_or_404(Room, id=room_id)
    user = get_object_or_404(User, id=user_id)

    if room.owner != request.user:  # Condition : le user actuel doit être
        # le propriétaire du salon.
        return render(request, 'main/403.html', status=403)

    invitation = RoomInvitation(user=user, room=room)
    invitation.save()
    print(invitation.id)

    return JsonResponse({'message': "Votre invitation a été envoyée à "
                                    "l'utilisateur."})


@login_required
@require_GET
def search_remove_user(request):
    search_term = request.GET.get('search_term', '')
    room_id = request.GET.get('room_id', '')
    room = get_object_or_404(Room, id=room_id)

    if room.owner != request.user:  # Condition : le user actuel doit être
        # le propriétaire du salon.
        return render(request, 'main/403.html', status=403)

    user = request.user
    room_users = User.objects.filter(
        Q(username__icontains=search_term) &
        Q(rooms__id=room_id) &
        ~Q(room__owner=user)
    )[:5]  # Q crée une condition de requête et ~Q crée la négation (NOT)
    # d'une condition de requête.
    search_results_html = render_to_string(
        'rooms/remove_users_search_results.html',
        {'room_id': room_id, 'search_results': room_users})

    return JsonResponse({'remove_users_search_results_html':search_results_html})


@login_required
@require_POST
def remove_user(request):
    room_id = request.POST.get('room_id', '')
    user_id = request.POST.get('user_id', '')
    room = get_object_or_404(Room, id=room_id)
    user = get_object_or_404(User, id=user_id)

    if room.owner != request.user:  # Condition : le user actuel doit être
        # le propriétaire du salon.
        return render(request, 'main/403.html', status=403)

    room.users.remove(user)

    return JsonResponse({'message': "L'utilisateur a été éjecté du salon."})


@login_required
@require_POST
def accept_pending_request(request):
    request_id = request.POST.get('request_id', '')
    pending_request = get_object_or_404(JoinRequest, id=request_id)

    pending_request.is_approved = True
    pending_request.save()
    pending_request.room.users.add(pending_request.user)

    return JsonResponse({'message': "La demande a été acceptée."})


@login_required
@require_POST
def reject_pending_request(request):
    request_id = request.POST.get('request_id', '')
    pending_request = get_object_or_404(JoinRequest, id=request_id)

    if pending_request.room.owner != request.user:  # Condition : le user
        # actuel doit être le propriétaire du salon.
        return render(request, 'main/403.html', status=403)

    pending_request.delete()

    return JsonResponse({'message': "La demande a été rejetée."})


# Génération dynamique de contenu----------------------------------------------
@login_required
@require_GET
def refresh_your_rooms(request):
    your_rooms = request.user.rooms.all()

    updated_your_rooms_html = render_to_string(
        "rooms/updated_your_rooms.html",
        {"your_rooms": your_rooms, "user": request.user})

    return JsonResponse({"updated_your_rooms_html": updated_your_rooms_html})


@login_required
@require_GET
def refresh_rooms_invitations(request):
    rooms_invitations = RoomInvitation.objects.filter(
            user=request.user).distinct()

    updated_rooms_invitations_html = render_to_string(
        "rooms/updated_rooms_invitations.html",
        {"rooms_invitations": rooms_invitations})

    return JsonResponse({"updated_rooms_invitations_html":
                         updated_rooms_invitations_html})


@login_required
@require_GET
def refresh_your_requests(request):
    your_requests = JoinRequest.objects.filter(
            user=request.user, is_approved=False).distinct()

    updated_your_requests_html = render_to_string(
        "rooms/updated_your_requests.html", {"your_requests": your_requests})

    return JsonResponse({"updated_your_requests_html":
                         updated_your_requests_html})


@login_required
@require_GET
def refresh_accepted_requests(request):
    accepted_requests = JoinRequest.objects.filter(
            user=request.user, is_approved=True).distinct()

    updated_accepted_requests_html = render_to_string(
        "rooms/updated_accepted_requests.html",
        {"accepted_requests": accepted_requests})

    return JsonResponse({"updated_accepted_requests_html":
                         updated_accepted_requests_html})


@login_required
@require_GET
def refresh_pending_requests(request):
    room_id = request.GET.get('room_id', '')
    room = get_object_or_404(Room, id=room_id)

    if room.owner != request.user:  # Condition : le user actuel doit être
        # le propriétaire du salon.
        return render(request, 'main/403.html', status=403)

    pending_requests = room.pending_join_requests()

    updated_pending_requests_html = render_to_string(
        "rooms/updated_pending_requests.html",
        {"pending_requests": pending_requests})

    return JsonResponse({"updated_pending_requests_html":
                         updated_pending_requests_html})


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