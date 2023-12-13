from django.urls import path, include
from . import views
from django.contrib.auth.views import LoginView, LogoutView

app_name = "users"
urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path("dashboard/", views.dashboard, name="dashboard"),
    path('accounts/', include("django.contrib.auth.urls")),
]

