from django.urls import path, include
from . import views

app_name = "users"
urlpatterns = [
    path('accounts/', include("django.contrib.auth.urls")),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('password_change/', views.CustomPasswordChangeView.as_view(),
         name='password_change'),
    path('password_change_done/', views.CustomPasswordChangeDoneView.as_view(),
         name='password_change_done'),
    path('password_reset/', views.CustomPasswordResetView.as_view(),
         name='password_reset'),
    path('password_reset_done/', views.CustomPasswordResetDoneView.as_view(),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         views.CustomPasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('reset/done/', views.CustomPasswordResetCompleteView.as_view(),
         name='password_reset_complete'),
    path("register/", views.CustomUserCreationView.as_view(), name="register"),
    path('profil/', views.ProfilView.as_view(), name='profil'),
]
