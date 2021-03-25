from decimal import Decimal
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from djstripe.models import Customer, PaymentMethod
from djstripe.enums import SubscriptionStatus

from .models import UserTeam
from .exceptions import NotEnoughTranscriptionsError


@api_view(['GET'])
def get_transcription(request):
    try:
        customer = Customer.objects.get(subscriber=request.user)
    except Customer.DoesNotExist:
        pass
    else:
        if (customer
                .subscriptions
                .filter(status=SubscriptionStatus.trialing)
                .exists()):
            return Response({"message": "You have got a transcription from trial subscription"},
                            status=status.HTTP_200_OK)
    try:
        request.user.decrement_transcriptions_count(1)
        request.user.save()
    except NotEnoughTranscriptionsError:
        # return Response({"message": "Not enough transcriptions"}, status=status.HTTP_400_BAD_REQUEST)
        customer, _ = Customer.get_or_create(subscriber=request.user)
        if PaymentMethod.objects.filter(customer=customer).exists():
            try:
                customer.charge(amount=Decimal(2), currency='usd')
            except Exception:
                return Response({"message": "Error is occurred while charging a fee"},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "Customer must add payment methods"},
                            status=status.HTTP_400_BAD_REQUEST)
    return Response({"message": "You have got a transcription"}, status=status.HTTP_200_OK)


@api_view(['GET'])
def team_get_transcription(request, team):
    try:
        user_teams = UserTeam.objects.filter(users=request.user, active=True)
        team = user_teams.get(name=team)
    except UserTeam.DoesNotExist:
        return Response({"message": "There is no team with such name and user"}, status=status.HTTP_404_NOT_FOUND)
    else:
        try:
            customer = Customer.objects.get(subscriber=team.owner)
        except Customer.DoesNotExist:
            pass
        else:
            if (customer
                    .subscriptions
                    .filter(status=SubscriptionStatus.trialing)
                    .exists()):
                return Response({"message": "You have got a transcription from team's trial subscription"},
                                status=status.HTTP_200_OK)
        try:
            team.owner.decrement_transcriptions_count(1)
            team.owner.save()
        except NotEnoughTranscriptionsError:
            # return Response({"message": "Not enough transcriptions in your team"}, status=status.HTTP_400_BAD_REQUEST)
            customer, _ = Customer.get_or_create(subscriber=team.owner)
            if PaymentMethod.objects.filter(customer=customer).exists():
                try:
                    customer.charge(amount=Decimal(2), currency='usd')
                except Exception:
                    return Response({"message": "Error is occurred while charging a fee"},
                                    status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"message": "Customer must add payment methods"},
                                status=status.HTTP_400_BAD_REQUEST)
    return Response({"message": "You have got a transcription from your team"}, status=status.HTTP_200_OK)


@api_view(['GET'])
def create_team(request):
    pass


@api_view(['GET'])
def delete_team(request):
    pass


@api_view(['GET'])
def team_add_users(request):
    pass


@api_view(['GET'])
def team_remove_users(request):
    pass
