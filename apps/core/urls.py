from django.urls import path

from . import views


urlpatterns = [
    path('create/', views.create_team),
    path('delete/', views.delete_team),
    path('add-users/', views.team_add_users),
    path('remove-users/', views.team_remove_users),
    path('<str:team>/get-transcription/', views.team_get_transcription),
]