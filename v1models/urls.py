from .views.tts import TTSAPIView

from django.urls import path

urlpatterns = [
    path("tts/", TTSAPIView.as_view(), name="tts"),
]

__all__ = ["urlpatterns"]