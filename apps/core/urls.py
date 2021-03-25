from django.urls import path

from .views import CreateTeamTranscriptionApiView


urlpatterns = [
    path('<str:team>/create-transcription/', CreateTeamTranscriptionApiView.as_view()),
]