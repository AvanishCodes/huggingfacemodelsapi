from diffusers import StableDiffusionPipeline
import torch
import uuid
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import FileResponse
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

IMAGE_GENERATION_FILES_DIR = "data/imagegeneration"

def generate_completions(prompt: str, filename: str):
    MODEL = "runwayml/stable-diffusion-v1-5"
    pipe = StableDiffusionPipeline.from_pretrained(MODEL, torch_dtype=torch.float32)
    image = pipe(prompt).images[0]
    filename = f"{IMAGE_GENERATION_FILES_DIR}/{filename}.png"
    image.save(filename)
    return filename




class ImageGenerationAPIView(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "prompt": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="The prompt for the image generation model.",
                )
            },
        ),
        operation_summary="Generate sentence completions",
        operation_description="Generate completions for the given input text using the GPT-2 model.",
    )
    def post(self, request):
        if "prompt" not in request.data:
            return Response(
                {"error": "No input text provided"}, status=status.HTTP_400_BAD_REQUEST
            )

        input_text = request.data["prompt"]
        uuid_str = str(uuid.uuid4())
        try:
            image_filename = generate_completions(input_text, uuid_str)
            return FileResponse(open(image_filename, 'rb'), as_attachment=True)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        # Perform sentence completions
