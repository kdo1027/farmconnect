"""
Pytest configuration and shared fixtures
"""
import pytest
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@pytest.fixture(autouse=True)
def reset_environment():
    """Reset environment variables before each test"""
    # Store original env vars
    original_env = os.environ.copy()

    yield

    # Restore original env vars
    os.environ.clear()
    os.environ.update(original_env)


@pytest.fixture
def mock_twilio_env(monkeypatch):
    """Mock Twilio environment variables"""
    monkeypatch.setenv('TWILIO_ACCOUNT_SID', 'test_account_sid')
    monkeypatch.setenv('TWILIO_AUTH_TOKEN', 'test_auth_token')
    return {
        'account_sid': 'test_account_sid',
        'auth_token': 'test_auth_token'
    }
