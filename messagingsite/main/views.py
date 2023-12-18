from django.views.generic.base import TemplateView


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
