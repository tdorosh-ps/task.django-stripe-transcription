from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import UserTeam
from .permissions import CanCreateTranscriptionPermission, CanCreateTeamTranscriptionPermission


class CreateTranscriptionApiView(APIView):
    permission_classes = (CanCreateTranscriptionPermission, )

    def get(self, request):
        request.user.decrement_transcriptions_count(1)
        request.user.save()
        return Response({"message": "You have got a transcription"}, status=status.HTTP_200_OK)


class CreateTeamTranscriptionApiView(APIView):
    permission_classes = (CanCreateTeamTranscriptionPermission, )

    def get(self, request, team):
        team_obj = UserTeam.objects.get(name=team, users=request.user, active=True)
        team_obj.owner.decrement_transcriptions_count(1)
        team_obj.owner.save()
        return Response({"message": "You have got a transcription from your team"}, status=status.HTTP_200_OK)
