import os
import uuid
import speech_recognition as sr
from pydub import AudioSegment
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated
from drf_yasg import openapi

STT_FILES_DIR = "data/stt"


def mp3_to_wav(mp3_file, wav_file):
    # Load MP3 file
    audio = AudioSegment.from_mp3(mp3_file)
    # Export as WAV
    audio.export(wav_file, format="wav")


def transcribe_audio(wav_file):
    # Initialize recognizer class
    recognizer = sr.Recognizer()
    # Read the audio file
    with sr.AudioFile(wav_file) as source:
        audio_data = recognizer.record(source)
    # Recognize the speech using PocketSphinx
    try:
        text = recognizer.recognize_sphinx(audio_data)
        return text
    except sr.UnknownValueError:
        return "PocketSphinx could not understand the audio"
    except sr.RequestError as e:
        return f"Error with PocketSphinx: {e}"


def convert_mp3_to_text(mp3_file):
    wav_file = "temp.wav"
    mp3_to_wav(mp3_file, wav_file)
    text = transcribe_audio(wav_file)
    return text


class STTAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "audio": openapi.Schema(
                    type=openapi.TYPE_FILE,
                    description="The audio file to be converted to text.",
                )
            },
        ),
        operation_summary="Convert speech to text",
        operation_description="Convert the given audio file to text using the Facebook Wav2Vec2 model.",
    )
    def post(self, request):
        if "file" not in request.FILES:
            return Response(
                {"error": "No file uploaded"}, status=status.HTTP_400_BAD_REQUEST
            )

        uploaded_file = request.FILES["file"]
        # Check if the file is an audio file with MP3 format
        if not uploaded_file.name.endswith(".mp3"):
            return Response(
                {"error": "Invalid file format. We currently support only MP3."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        uuid_str = str(uuid.uuid4())

        # Save the uploaded file
        file_path = os.path.join(STT_FILES_DIR, f"{uuid_str}.mp3")
        os.makedirs(STT_FILES_DIR, exist_ok=True)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.read())

        # Convert the MP3 file to text
        try:
            text = convert_mp3_to_text(file_path)
            return Response({"text": text, "id": uuid_str}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": f"An error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
