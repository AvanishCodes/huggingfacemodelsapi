from .views.tts import TTSAPIView
# from .views.stt import STTAPIView
from .views.completions import SentenceCompletionsAPIView
from .views.imagegeneration import ImageGenerationAPIView

from django.urls import path

urlpatterns = [
    path("gtts/tts/", TTSAPIView.as_view(), name="tts"),
    # path("stt/", STTAPIView.as_view(), name="stt"),
    path("gpt2/completions/", SentenceCompletionsAPIView.as_view(), name="completions"),
    path("diffusion/generations/", ImageGenerationAPIView.as_view(), name="generations"),
]

__all__ = ["urlpatterns"]