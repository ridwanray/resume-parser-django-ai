import os

from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import UploadedFile

VALID_EXTENSIONS = [".pdf", ".docx", ".doc"]


def validate_file_extension(file_object: UploadedFile):
    ext: str = os.path.splitext(file_object.name)[1]
    if ext.lower() not in VALID_EXTENSIONS:
        raise ValidationError(f"Only PDF and Docx formats are allowed. {ext} detected")
    return ext


def validate_file_size(file_object: UploadedFile):
    MAX_UPLOAD_SIZE = 2_096_152  # in bytes
    if file_object.size > MAX_UPLOAD_SIZE:
        raise ValidationError(
            f"Max file size is 2MB. You uploaded {(file_object.size/1_048_576):.2f}MB"
        )
