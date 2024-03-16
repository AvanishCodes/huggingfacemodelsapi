from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from rest_framework import status
from unittest.mock import patch


class TTSAPIViewTests(APITestCase):
    def setUp(self):
        self.client = APIClient()

    def test_tts_conversion_success(self):
        url = reverse("tts")
        data = {"text": "Hello, world!", "lang": "en"}
        response = self.client.post(url, data, format="json",)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Content-Disposition", response.headers)

    def test_missing_text_input(self):
        url = reverse("tts")
        data = {"lang": "en"}
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_tts_conversion_failure(self):
        url = reverse("tts")
        data = {"text": "Hello, world!", "lang": "something"}
        with patch("gtts.gTTS.save", side_effect=Exception("Mocked error")), patch(
            "gtts.gTTS.__init__"
        ), patch("os.makedirs"):
            response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
