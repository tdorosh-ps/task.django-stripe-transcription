from rest_framework import permissions

from .models import UserTeam


class CanCreateTranscriptionPermission(permissions.BasePermission):
    message = 'Transcription create not allowed.'

    def has_permission(self, request, view):
        if request.user.transcriptions_count > 0:
            return True
        return False


class CanCreateTeamTranscriptionPermission(permissions.BasePermission):
    message = 'Team transcription create not allowed.'

    def has_permission(self, request, view):
        try:
            user_teams = UserTeam.objects.filter(users=request.user, active=True)
            team = user_teams.get(name=view.kwargs['team'])
        except UserTeam.DoesNotExist:
            return False
        else:
            if team.owner.transcriptions_count > 0:
                return True
        return False
