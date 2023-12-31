from django.urls import path
from . import views

app_name = "main"
urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("administration/", views.AdminView.as_view(), name="administration"),
    path('search_delete_user/', views.search_delete_user,
         name='search_delete_user'),
    path('delete_user/', views.delete_user, name='delete_user'),
    path("support/", views.HelpView.as_view(), name="help"),
    path("error_400/", views.error_400, name="error_400"),
    path("error_403/", views.error_403, name="error_403"),
    path("error_404/", views.error_404, name="error_404"),
    path("error_405/", views.error_405, name="error_405"),
    path("error_500/", views.error_500, name="error_500"),
]
