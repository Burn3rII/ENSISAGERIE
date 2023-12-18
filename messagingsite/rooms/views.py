from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from django.template.loader import render_to_string
from .forms import RoomCreationForm
from .models import Room


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
        rooms = Room.objects.filter(name__icontains=search_term)
        search_results_html = render_to_string('rooms/search_results.html',
                                               {'search_results': rooms})

        return JsonResponse({'search_results_html': search_results_html})
    else:
        return JsonResponse({'error': 'Méthode non autorisée'})
