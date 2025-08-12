import os
import pytest
from client import FavQsCli
from dotenv import load_dotenv

from custom_errors import FavQsAuthError

load_dotenv()

@pytest.fixture(scope="session")
def api_token():
    if not (token := os.getenv("FAVQS_API_KEY", "").strip()):
        raise FavQsAuthError("Missing FAVQS_API_KEY environment variable")
    return token


@pytest.fixture
def client(api_token):
    return FavQsCli(api_token=api_token)
