from django.urls import path
from . import views

app_name = "rooms"
urlpatterns = [
    path("create/", views.RoomCreationView.as_view(),
         name="create"),
    path("detail/<int:room_id>/", views.RoomDetailView.as_view(),
         name="detail"),
    path('search/', views.search_rooms, name='search'),
    path('send_message/', views.send_message, name='send_message'),
    path('load_messages/', views.load_messages, name='load_messages'),
    path('last_message_date/', views.last_message_date, name='last_message_date'),
]
