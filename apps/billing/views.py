from datetime import timedelta, datetime
from decimal import Decimal

from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from djstripe.models import Customer, Price, Subscription, PaymentMethod
from djstripe.enums import SubscriptionStatus

from apps.core.exceptions import NotEnoughTranscriptionsError


@api_view(['POST'])
def subscribe(request):
    customer, _ = Customer.get_or_create(subscriber=request.user)
    try:
        price = Price.objects.get(nickname=request.data['price'])
    except Price.DoesNotExist:
        return Response({"message": "Price doesnot exist"}, status=status.HTTP_404_NOT_FOUND)
    if PaymentMethod.objects.filter(customer=customer).exists():
        try:
            kwargs = {'trial_end': datetime.now() + timedelta(7), 'collection_method': 'send_invoice',
                      'days_until_due': 7}
            customer.subscribe(price=price, **kwargs)
        except Exception:
            return Response({"message": "There was an error during subscribing"},
                            status=status.HTTP_400_BAD_REQUEST)
        else:
            request.user.increment_transcriptions_count(price.transform_quantity['divide_by'])
            request.user.save()
            return Response({"message": "Successfully subscribed"}, status=status.HTTP_200_OK)
    else:
        return Response({"message": "Customer must add payment methods"},
                        status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def unsubscribe(request):
    try:
        customer = Customer.objects.get(subscriber=request.user)
    except Customer.DoesNotExist:
        return Response({"message": "Customer doesnot exist"}, status=status.HTTP_404_NOT_FOUND)
    try:
        subscription = Subscription.objects.exclude(status=SubscriptionStatus.canceled)\
            .get(id=request.data['subscription_id'], customer=customer)
        subscription.cancel()
    except Subscription.DoesNotExist:
        return Response({"message": "Subscription doesnot exist"}, status=status.HTTP_404_NOT_FOUND)
    except Exception:
        return Response({"message": "There was an error during cancel subscription"},
                        status=status.HTTP_400_BAD_REQUEST)
    else:
        if subscription.status == SubscriptionStatus.trialing:
            try:
                request.user.decrement_transcriptions_count(subscription.plan.transform_usage['divide_by'])
            except NotEnoughTranscriptionsError:
                request.user.transcriptions_count = 0
            request.user.save()
        return Response({"message": "Successfully unsubscribed"}, status=status.HTTP_200_OK)


@api_view(['POST'])
def charge(request):
    customer, _ = Customer.get_or_create(subscriber=request.user)
    if PaymentMethod.objects.filter(customer=customer).exists():
        try:
            customer.charge(amount=Decimal(request.data['amount']), currency=request.data['currency'])
        except Exception:
            return Response({"message": "There was an error during charging a fee"},
                            status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "Successfully charged"}, status=status.HTTP_200_OK)
    else:
        return Response({"message": "Customer must add payment methods"},
                        status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def add_card(request):
    stripe_token = request.data['stripe_token']
    customer, _ = Customer.get_or_create(subscriber=request.user)
    try:
        customer.add_card(stripe_token)
    except Exception:
        return Response({"message": "There was an error during adding a card"},
                        status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"message": "Card was successfully added"}, status=status.HTTP_200_OK)


