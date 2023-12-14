from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView

class HomeView(TemplateView):
    template_name = "main/index.html"

class HelpView(TemplateView):
    template_name = "main/help.html"
