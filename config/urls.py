from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken import views

from apps.core.views import CreateTranscriptionApiView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api-token-auth/', views.obtain_auth_token),
    path('stripe/', include('djstripe.urls', namespace='djstripe')),

    path('api/v1/create-transcription/', CreateTranscriptionApiView.as_view()),
    path('api/v1/billing/', include(('apps.billing.urls', 'billing'), namespace='billing')),
    path('api/v1/teams/', include(('apps.core.urls', 'core'), namespace='teams')),
]
