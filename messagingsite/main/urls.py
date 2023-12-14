from django.urls import path
from . import views

app_name = "main"
urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("support/", views.HelpView.as_view(), name="help"),
]