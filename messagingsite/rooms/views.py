import os
import json
from django.templatetags.static import static
from django.views.generic.edit import CreateView
from django.db.models import Q, Count
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


# Sur la page d'accueil--------------------------------------------------------
@login_required  # Si le user n'est pas connecté, redirige vers la page de
# connexion
def detail(request, room_id):
    room = get_object_or_404(Room, pk=room_id)

    if request.user not in room.users.all():  # Le user actuel doit faire
        # partie du salon.
        return render(request, 'main/403.html', status=403)

    context = {'room': room}
    return render(request, 'rooms/detail.html', context)


@login_required
@require_POST
def accept_invitation(request):
    invitation_id = request.POST.get('invitation_id', '')
    invitation = get_object_or_404(RoomInvitation, id=invitation_id)

    if invitation.user != request.user:  # L'invitation doit être adressée
        # au user actuel
        return render(request, 'main/403.html', status=403)

    invitation.room.users.add(invitation.user)
    invitation.delete()

    return JsonResponse({'message': "Invitation acceptée !"})


@login_required
@require_POST
def reject_invitation(request):
    invitation_id = request.POST.get('invitation_id', '')
    invitation = get_object_or_404(RoomInvitation, id=invitation_id)

    if invitation.user != request.user:  # L'invitation doit être adressée
        # au user actuel
        return render(request, 'main/403.html', status=403)

    invitation.delete()

    return JsonResponse({'message': "Invitation refusée."})


@login_required
@require_POST
def delete_accepted_request(request):
    request_id = request.POST.get('request_id', '')
    accepted_request = get_object_or_404(JoinRequest, id=request_id)

    if accepted_request.user != request.user:  # La requête doit avoir été
        # créée par le user actuel
        return render(request, 'main/403.html', status=403)

    accepted_request.delete()

    return JsonResponse({'message': "La demande a été détruite."})


@login_required
@require_GET
def search_room(request):
    search_term = request.GET.get('search_term', '')
    user = request.user
    rooms = Room.objects.filter(
        Q(name__icontains=search_term) & ~Q(users=user) &
        ~Q(joinrequest__user=user) & ~Q(roominvitation__user=user)
    )[:5]  # On ne garde que les rooms pour lesquelles le user n'est pas
    # déjà dedans, il n'y a pas déjà une demande de rejoindre et il n'y a
    # pas déjà une invitation.
    search_results_html = render_to_string(
        'rooms/rooms_search_results.html',
        {'search_results': rooms, "user": request.user})

    return JsonResponse({'rooms_search_results_html': search_results_html})


@login_required
@require_POST
def join_room(request):
    room_id = request.POST.get('room_id', '')
    room = get_object_or_404(Room, id=room_id)

    if room.private:
        return JsonResponse({'message': 'Ce salon est privé. Vous devez '
                                        'faire une demande.'})

    if request.user in room.users_banned.all():
        return JsonResponse({
            'message': 'Vous avez été banni de ce salon. Vous devez désormais '
                       'faire une demande avant d\'entrer à nouveau.'})

    RoomInvitation.objects.filter(user=request.user, room=room).delete()
    JoinRequest.objects.filter(user=request.user, room=room).delete()
    room.users.add(request.user)

    return JsonResponse({'message': 'Vous avez rejoint le salon!'})


@login_required
@require_POST
def request_to_join(request):
    room_id = request.POST.get('room_id', '')
    room = get_object_or_404(Room, id=room_id)

    if not room.private and request.user not in room.users_banned.all():
        return JsonResponse({'message': 'Ce salon est publique. Pas besoin de '
                                        'demande.'})

    if room.users.filter(id=request.user.id).exists():
        return JsonResponse({'message': 'Vous êtes déjà membre de ce salon.'})

    if RoomInvitation.objects.filter(user=request.user,
                                     room=room).exists():
        return JsonResponse({'message': 'Vous avez déjà reçu une invitation '
                                        'pour ce salon.'})

    if JoinRequest.objects.filter(user=request.user, room=room).exists():
        return JsonResponse({'message': 'Vous avez déjà soumis une demande '
                                        'pour rejoindre ce salon.'})

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
def statistics(request, room_id):
    room = Room.objects.get(id=room_id)

    # Statistiques générales
    total_messages = Message.objects.filter(room=room).count()
    total_users = room.users.count()

    # Statistiques des utilisateurs
    active_users = room.users.filter(message__room=room).distinct().count()

    # Activité temporelle
    messages_per_day = Message.objects.filter(room=room).extra(
        select={'day': 'date(publication_date)'}
    ).values('day').annotate(count=Count('id'))

    context = {
        'room': room,
        'total_messages': total_messages,
        'total_users': total_users,
        'active_users': active_users,
        'messages_per_day': messages_per_day,
    }

    return render(request, 'rooms/room_statistics.html', context)


@login_required
def user_management(request, room_id):
    room = get_object_or_404(Room, pk=room_id)

    if room.owner != request.user:  # Le user actuel doit être le
        # propriétaire du salon.
        return render(request, 'main/403.html', status=403)

    context = {'room': room}

    return render(request, 'rooms/user_management.html', context)


@login_required
@require_POST
def send_message(request):
    room_id = request.POST.get('room_id')
    room = get_object_or_404(Room, pk=room_id)

    if not room.users.filter(id=request.user.id).exists():
        return JsonResponse({'message': 'Vous ne faites pas partie de ce '
                                        'salon.'})

    message_content = request.POST.get('message')

    Message.objects.create(room=room, sender=request.user,
                           text=message_content)

    return JsonResponse({'message': 'Le message a été envoyé.'})


@login_required
@require_GET
def load_messages(request):
    room_id = request.GET.get('room_id')
    room = get_object_or_404(Room, pk=room_id)

    if not room.users.filter(id=request.user.id).exists():
        return JsonResponse({'message': 'Vous ne faites pas partie de ce '
                                        'salon.'})

    message_number = int(request.GET.get('message_number'))
    message_count = Message.objects.filter(room=room).count()

    if message_number > message_count:
        message_number = message_count

    messages = Message.objects.filter(room=room).order_by(
        '-publication_date').reverse()[message_count - message_number:]

    return render(request, 'rooms/messages.html',
                  {'messages': messages, 'room': room})


@login_required
@require_GET
def load_all_messages(request):
    room_id = request.GET.get('room_id')
    room = get_object_or_404(Room, pk=room_id)

    if not room.users.filter(id=request.user.id).exists():
        return JsonResponse({'message': 'Vous ne faites pas partie de ce '
                                        'salon.'})

    messages = Message.objects.filter(room=room).order_by(
        '-publication_date').reverse()

    return render(request, 'rooms/messages.html',
                  {'messages': messages, 'room': room})


@login_required
@require_GET
def get_message_number(request):
    room_id = request.GET.get('room_id')
    room = get_object_or_404(Room, pk=room_id)
    message_number = Message.objects.filter(room=room).count()

    return JsonResponse({'message_number': message_number})


@login_required
@require_POST
def remove_message(request):
    message_id = request.POST.get('message_id', '')
    message = get_object_or_404(Message, id=message_id)

    if request.user != message.room.owner and request.user != message.sender:
        # Le user actuel doit être le owner ou le message doit appartenir au
        # user actuel
        return render(request, 'main/403.html', status=403)

    if message.is_deleted:
        return JsonResponse({'message': 'Ce message a déjà été supprimé.'})

    message.text = "Ce message a été supprimé."
    message.is_deleted = True
    message.save()

    return JsonResponse({'message': "Le message a été supprimé."})


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

    if room.owner != request.user:  # Le user actuel doit être le
        # propriétaire du salon.
        return render(request, 'main/403.html', status=403)

    room_users = User.objects.filter(
        Q(username__icontains=search_term) & ~Q(rooms__id=room_id) &
        ~Q(roominvitation__room_id=room_id) &
        ~Q(joinrequest__room_id=room_id))[:5]  # On ne garde que les
    # users qui ne sont pas déjà dans la room, qui n'ont pas déjà reçu
    # une invitation et qui n'ont pas déjà fait une demande.
    search_results_html = render_to_string(
        'rooms/invite_users_search_results.html',
        {'room_id': room_id, 'search_results': room_users})

    return JsonResponse({'invite_users_search_results_html':
                         search_results_html})


@login_required
@require_POST
def invite(request):
    room_id = request.POST.get('room_id', '')
    user_id = request.POST.get('user_id', '')
    room = get_object_or_404(Room, id=room_id)
    user = get_object_or_404(User, id=user_id)

    if room.owner != request.user:  # Le user actuel doit être le
        # propriétaire du salon.
        return render(request, 'main/403.html', status=403)

    if room.users.filter(id=user.id).exists():
        return JsonResponse({'message': "Le user est déjà membre de ce "
                                        "salon."})

    if RoomInvitation.objects.filter(user=user, room=room).exists():
        return JsonResponse({'message': "Le user a déjà reçu une invitation "
                                        "pour ce salon."})

    if JoinRequest.objects.filter(user=user, room=room).exists():
        return JsonResponse({'message': "Le user a déjà soumis une demande "
                                        "pour rejoindre ce salon."})

    invitation = RoomInvitation(user=user, room=room)
    invitation.save()
    return JsonResponse({'message': "Votre invitation a été envoyée à "
                                    "l'utilisateur."})


@login_required
@require_GET
def search_remove_user(request):
    search_term = request.GET.get('search_term', '')
    room_id = request.GET.get('room_id', '')
    room = get_object_or_404(Room, id=room_id)

    if room.owner != request.user:  # Le user actuel doit être le
        # propriétaire du salon.
        return render(request, 'main/403.html', status=403)

    room_users = User.objects.filter(
        Q(username__icontains=search_term) & Q(rooms__id=room_id) &
        ~Q(room__owner=request.user)
    )[:5]  # On ne garde que les users qui sont dans le salon, sauf le owner
    search_results_html = render_to_string(
        'rooms/remove_users_search_results.html',
        {'room_id': room_id, 'search_results': room_users})

    return JsonResponse({'remove_users_search_results_html':
                         search_results_html})


@login_required
@require_POST
def remove_user(request):
    room_id = request.POST.get('room_id', '')
    user_id = request.POST.get('user_id', '')
    room = get_object_or_404(Room, id=room_id)
    user = get_object_or_404(User, id=user_id)

    if room.owner != request.user and user != request.user:  # Le user actuel
        # doit être le propriétaire du salon ou la personne éjectée dans le
        # cas où le user quitte lui même le groupe
        return render(request, 'main/403.html', status=403)

    if not room.users.filter(id=user.id).exists():
        return JsonResponse({'message': "L'utilisateur n'est pas dans ce "
                                        "salon."})

    if user == room.owner:
        return JsonResponse({'message': "Vous ne pouvez pas éjecter le "
                                        "propriétaire du salon."})

    JoinRequest.objects.filter(user=user, room=room).delete()
    room.users_banned.add(user)
    room.users.remove(user)

    if user == request.user:
        return JsonResponse(
            {'message': "Vous avez quitté le groupe."})

    return JsonResponse({'message': "L'utilisateur a été éjecté du salon."})


@login_required
@require_POST
def accept_pending_request(request):
    request_id = request.POST.get('request_id', '')
    pending_request = get_object_or_404(JoinRequest, id=request_id)

    if pending_request.room.owner != request.user:  # Le user actuel doit
        # être le propriétaire du salon.
        return render(request, 'main/403.html', status=403)

    pending_request.is_approved = True
    pending_request.save()
    pending_request.room.users.add(pending_request.user)

    return JsonResponse({'message': "La demande a été acceptée."})


@login_required
@require_POST
def reject_pending_request(request):
    request_id = request.POST.get('request_id', '')
    pending_request = get_object_or_404(JoinRequest, id=request_id)

    if pending_request.room.owner != request.user:  # Le user actuel doit
        # être le propriétaire du salon.
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

    if room.owner != request.user:  # Le user actuel doit être le
        # propriétaire du salon.
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