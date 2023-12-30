from django.urls import path
from . import views

app_name = "rooms"
urlpatterns = [
    # Page d'accueil-----------------------------------------------------------
    path("detail/<int:room_id>/", views.detail,
         name="detail"),
    path('accept_invitation/', views.accept_invitation,
         name='accept_invitation'),
    path('reject_invitation/', views.reject_invitation,
         name='reject_invitation'),
    path('delete_accepted_request/', views.delete_accepted_request,
         name='delete_accepted_request'),
    path('search_room/', views.search_room, name='search_room'),
    path('join_room/', views.join_room, name='join_room'),
    path('request_to_join/', views.request_to_join,
         name='request_to_join'),
    # Page de création de salon------------------------------------------------
    path("create/", views.RoomCreationView.as_view(),
         name="create"),
    # Page d'un salon----------------------------------------------------------
    path("user_management/<int:room_id>/", views.user_management,
         name="user_management"),
    path('send_message/', views.send_message, name='send_message'),
    path('last_message_date/', views.last_message_date,
         name='last_message_date'),
    path('load_messages/', views.load_messages, name='load_messages'),
    # Page de gestion des utilisateurs d'un salon------------------------------
    path('search_invite_user/', views.search_invite_user,
         name='search_invite_user'),
    path('invite/', views.invite, name='invite'),
    path('search_remove_user/', views.search_remove_user,
         name='search_remove_user'),
    path('remove_user/', views.remove_user, name='remove_user'),
    path('accept_pending_request/', views.accept_pending_request,
         name='accept_pending_request'),
    path('reject_pending_request/', views.reject_pending_request,
         name='reject_pending_request'),
    # Génération dynamique de contenu------------------------------------------
    path('refresh_your_rooms/', views.refresh_your_rooms,
         name='refresh_your_rooms'),
    path('refresh_rooms_invitations/', views.refresh_rooms_invitations,
         name='refresh_rooms_invitations'),
    path('refresh_your_requests/', views.refresh_your_requests,
         name='refresh_your_requests'),
    path('refresh_accepted_requests/', views.refresh_accepted_requests,
         name='refresh_accepted_requests'),
    path('refresh_pending_requests/', views.refresh_pending_requests,
         name='refresh_pending_requests'),
]
