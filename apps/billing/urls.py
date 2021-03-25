from django.urls import path

from . import views


urlpatterns = [
    path('subscribe/', views.subscribe),
    path('unsubscribe/', views.unsubscribe),
    path('charge/', views.charge),
    path('add-card/', views.add_card),
]
