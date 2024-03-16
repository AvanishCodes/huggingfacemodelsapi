from rest_framework.test import APIClient, APITestCase
from rest_framework import status
import os
from django.urls import reverse


class STTAPITestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()

    def test_stt_api_with_invalid_file_format(self):
        url = reverse("stt")
        # Prepare a sample text file instead of an MP3 file
        file_path = "test.txt"
        with open(file_path, "w") as f:
            f.write("This is a sample text file.")

        # Make a POST request to the STT API
        with open(file_path, "rb") as f:
            response = self.client.post(url, {"file": f}, format="multipart")

        # Clean up the sample text file
        os.remove(file_path)

        # Assert the response status code
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Assert the response contains the expected error message
        self.assertEqual(
            response.data["error"],
            "Invalid file format. We currently support only MP3.",
        )

    # Add more test cases as needed
