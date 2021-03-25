from django.urls import path

from . import views


urlpatterns = [
    path('subscribe/', views.subscribe),
    path('unsubscribe/', views.unsubscribe),
    path('charge-transcription/', views.charge_transcription),
    path('add-card/', views.add_card),
]
