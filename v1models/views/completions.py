from transformers import GPT2Tokenizer, GPT2LMHeadModel
import uuid
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

STT_FILES_DIR = "data/stt"


def generate_completions(prompt, num_completions=1, max_length=50):
    # Load pre-trained GPT-2 model and tokenizer
    tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
    model = GPT2LMHeadModel.from_pretrained("gpt2")

    # Tokenize the prompt
    input_ids = tokenizer.encode(prompt, return_tensors="pt", add_special_tokens=True)

    # Generate completions using beam search
    outputs = model.generate(
        input_ids,
        max_length=max_length,
        num_return_sequences=num_completions,
        temperature=0.7,
        top_k=50,
        top_p=0.95,
        repetition_penalty=1.0,
        pad_token_id=tokenizer.eos_token_id,
        early_stopping=True,
        num_beams=5  # Number of beams for beam search
    )
    # Decode and return completions
    completions = [
        tokenizer.decode(output, skip_special_tokens=True) for output in outputs
    ]
    _ = []
    for i, completion in enumerate(completions):
        [_.append(item) for item in completion.split('\n\n')]
    _.sort()
    return _



class SentenceCompletionsAPIView(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "text": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="The input text to be completed.",
                )
            },
        ),
        operation_summary="Generate sentence completions",
        operation_description="Generate completions for the given input text using the GPT-2 model.",
    )
    def post(self, request):
        if "text" not in request.data:
            return Response(
                {"error": "No input text provided"}, status=status.HTTP_400_BAD_REQUEST
            )

        input_text = request.data["text"]
        uuid_str = str(uuid.uuid4())
        try:
            # Generate sentence completions
            completions = generate_completions(
                input_text, num_completions=3, max_length=50
            )
            return Response(
                {"completions": completions, "uuid": uuid_str},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        # Perform sentence completions
