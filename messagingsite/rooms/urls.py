from django.urls import path
from . import views

app_name = "rooms"
urlpatterns = [
    path("create_room/", views.RoomCreationView.as_view(),
         name="create"),
    path("roomdetail/<int:room_id>/", views.RoomDetailView.as_view(),
         name="detail"),
    path('search/', views.search_rooms, name='search'),
]
