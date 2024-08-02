from django.test.client import Client
import pytest


@pytest.fixture
def client():
    return Client()