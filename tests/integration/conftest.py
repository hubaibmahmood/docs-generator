import os

import pytest
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Ensure GEMINI_API_KEY is set in the environment for tests
@pytest.fixture(scope="session", autouse=True)
def set_gemini_api_key_for_tests():
    if "GEMINI_API_KEY" not in os.environ:
        os.environ["GEMINI_API_KEY"] = "dummy_test_key"
    yield
    if os.environ["GEMINI_API_KEY"] == "dummy_test_key":
        del os.environ["GEMINI_API_KEY"]
