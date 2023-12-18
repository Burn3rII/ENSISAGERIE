from django.views.generic.base import TemplateView
from django.shortcuts import render


class HomeView(TemplateView):
    template_name = "main/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            context["your_rooms"] = self.request.user.rooms.all()[:5]
        else:
            context["your_rooms"] = []

        return context


class HelpView(TemplateView):
    template_name = "main/help.html"

def error_400(request, exception):
    return render(request, 'main/400.html', status=400)

def error_403(request, exception):
    return render(request, 'main/403.html', status=403)

def error_404(request, exception):
    return render(request, 'main/404.html', status=404)

def error_500(request):
    return render(request, 'main/500.html', status=500)