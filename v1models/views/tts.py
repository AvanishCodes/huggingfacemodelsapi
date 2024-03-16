import os
import uuid
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import FileResponse
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.permissions import IsAuthenticated
from gtts import gTTS

TTS_FILES_DIR = "data/tts"


class TTSAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "text": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="The text to be converted to speech.",
                ),
                "lang": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="The language of the text. Default is 'en'.",
                ),
            },
            required=["text"],
        ),
        operation_summary="Convert text to speech",
        operation_description="Convert the given text to speech using the Facebook Wav2Vec2 model.",
    )
    def post(self, request):
        text = request.data.get("text")
        lang = request.data.get("lang") or "en"
        audio_id = str(uuid.uuid4())

        # Basic input validation
        if not text:
            return Response(
                {"error": "Text input is required."}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Load text-to-speech pipeline
            tts = gTTS(text=text, lang=lang, slow=False)
            file_path = f"{TTS_FILES_DIR}/{audio_id}.mp3"
            os.makedirs(TTS_FILES_DIR, exist_ok=True)
            tts.save(file_path)
            # Return audio and force download in browser
            return FileResponse(open(file_path, "rb"), as_attachment=True)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


__all__ = ["TTSAPIView"]
