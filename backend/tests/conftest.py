"""Test fixtures: test client, mock auth."""

from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client():
    """FastAPI test client."""
    return TestClient(app)


@pytest.fixture
def auth_client(client):
    """Test client with mocked auth — returns clerk_id 'test_user_123'."""
    with patch("app.auth.middleware.get_current_user_id", return_value="test_user_123"):
        yield client
