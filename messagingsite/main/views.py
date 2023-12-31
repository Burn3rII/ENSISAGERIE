from django.views.generic.base import TemplateView
from django.db.models import Q
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import transaction
from django.views.decorators.http import require_GET, require_POST

from django.contrib.auth.models import User
from rooms.models import Room, Message, JoinRequest, RoomInvitation


def superuser_required(user):
    return user.is_superuser


superuser_required_decorator = user_passes_test(superuser_required)


class HomeView(TemplateView):
    template_name = "main/index.html"


@method_decorator(login_required, name='dispatch')
@method_decorator(superuser_required_decorator, name='dispatch')
class AdminView(TemplateView):
    template_name = "main/admin.html"


@login_required
@superuser_required_decorator
@require_GET
def search_delete_user(request):
    print("DSDFS")
    search_term = request.GET.get('search_term', '')

    users = User.objects.filter(
        Q(username__icontains=search_term) & Q(is_superuser=False))[:5]
    # On ne garde que les users qui ne sont pas des superusers
    search_results_html = render_to_string(
        'main/delete_users_search_results.html',
        {'search_results': users})

    return JsonResponse({'delete_users_search_results_html':
                         search_results_html})


@login_required
@superuser_required_decorator
@require_POST
@transaction.atomic  # Permet de faire en sorte que si il y a une erreur,
# tous les changements effectués dans cette fonction ne sont pas pris en
# compte.
def delete_user(request):
    user_id = request.POST.get('user_id', '')
    user = get_object_or_404(User, id=user_id)

    if user.is_superuser:
        return JsonResponse({'message': "Vous ne pouvez pas éjecter un "
                                        "administrateur."})

    Message.objects.filter(sender=user).delete()
    JoinRequest.objects.filter(user=user).delete()
    RoomInvitation.objects.filter(user=user).delete()

    rooms_owned = Room.objects.filter(owner=user)
    for room in rooms_owned:
        room.owner = request.user
        room.save()

    user.delete()

    return JsonResponse(
        {'message': "L'utilisateur a été supprimé, ses messages supprimés et "
                    "vous êtes désormais propriétaire des salons qu'il "
                    "possédait."})


class HelpView(TemplateView):
    template_name = "main/help.html"


def error_400(request, exception):
    return render(request, 'main/400.html', status=400)


def error_403(request, exception):
    return render(request, 'main/403.html', status=403)


def error_404(request, exception):
    return render(request, 'main/404.html', status=404)


def error_405(request, exception):
    return render(request, 'main/405.html', status=405)


def error_500(request):
    return render(request, 'main/500.html', status=500)