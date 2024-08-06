from unittest.mock import MagicMock

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test.client import Client
from django.urls import reverse


def test_home(client: Client):
    url = reverse("home_page")
    response = client.get(url)
    assert response.status_code == 200
    assert b"Resume Parser" in response.content


class TestUploadResume:
    upload_resume_url = reverse("upload_resume")

    def test_upload_resume_invalid_extension(self, client: Client):
        invalid_file = SimpleUploadedFile("test.txt", b"File content")
        response = client.post(
            self.upload_resume_url, {"file": invalid_file}, format="multipart"
        )
        assert response.status_code == 400
        assert "error" in response.json()

    def test_upload_pdf_file(
        self, client: Client, mock_invoke_model: MagicMock, generate_pdf_file
    ):
        with open(generate_pdf_file, "rb") as uploaded_file:
            response = client.post(
                self.upload_resume_url, {"file": uploaded_file}, format="multipart"
            )

        assert response.status_code == 200
        mock_invoke_model.assert_called_once()
        call_arguments: dict = mock_invoke_model.call_args.kwargs
        assert call_arguments.get("contentType") == "application/json"
        assert call_arguments.get("modelId") == "meta.llama2-70b-chat-v1"

    def test_upload_doc_file(
        self, client: Client, mock_invoke_model: MagicMock, generate_doc_file
    ):
        with open(generate_doc_file, "rb") as uploaded_file:
            response = client.post(
                self.upload_resume_url, {"file": uploaded_file}, format="multipart"
            )
        assert response.status_code == 200
        mock_invoke_model.assert_called_once()
        call_arguments: dict = mock_invoke_model.call_args.kwargs
        assert call_arguments.get("contentType") == "application/json"
        assert call_arguments.get("modelId") == "meta.llama2-70b-chat-v1"
