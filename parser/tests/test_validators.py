from parser.validators import validate_file_extension, validate_file_size

import pytest
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile


@pytest.mark.parametrize("extension, is_exception_expected", [
    ("csv", True),
    ("mp4", True),
    ("mp3", True),
    ("pdf", False),
    ("doc", False),
    ("docx", False),
])
def test_validate_file_extension(extension, is_exception_expected):
    file = SimpleUploadedFile(name=f"sample-file.{extension}", content=b"Note")
    if is_exception_expected:
        with pytest.raises(ValidationError, match="Only PDF and Docx formats are allowed."):
            validate_file_extension(file)
    else:
        assert validate_file_extension(file)


@pytest.mark.parametrize("file_size, is_exception_expected", [
    (3_097_152, True),
    (6_097_152, True),
    (2_000_000, False),
])
def test_validate_file_size(file_size, is_exception_expected):
    file = SimpleUploadedFile(name="sample-file.pdf", content=b"Note")
    file.size = file_size
    if is_exception_expected:
        with pytest.raises(ValidationError, match="Max file size is 2MB"):
            validate_file_size(file)
    else:
        assert not validate_file_size(file)