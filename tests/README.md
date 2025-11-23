# FarmConnect Unit Tests

This directory contains comprehensive unit tests for the FarmConnect WhatsApp chatbot application.

## Test Structure

```
tests/
├── __init__.py              # Package initialization
├── conftest.py              # Shared pytest fixtures and configuration
├── test_data_store.py       # Tests for DataStore class
├── test_chatbot.py          # Tests for FarmConnectBot class
└── test_chatbot_simple.py   # Tests for SimpleFarmConnectBot class
```

## Running Tests

### Run all tests
```bash
pytest
```

### Run with coverage report
```bash
pytest --cov=. --cov-report=html
```

### Run specific test file
```bash
pytest tests/test_data_store.py
```

### Run specific test class
```bash
pytest tests/test_data_store.py::TestDataStoreUserManagement
```

### Run specific test function
```bash
pytest tests/test_data_store.py::TestDataStoreUserManagement::test_create_user_farmer
```

### Run with verbose output
```bash
pytest -v
```

### Run tests matching a pattern
```bash
pytest -k "farmer"
```

## Test Coverage

The test suite covers:

### DataStore Tests (`test_data_store.py`)
- ✅ User creation and management (farmers and farm owners)
- ✅ User profile updates
- ✅ Conversation state management
- ✅ Job creation and retrieval
- ✅ Job status updates
- ✅ Job matching and filtering
- ✅ Data persistence across instances

### FarmConnectBot Tests (`test_chatbot.py`)
- ✅ Welcome flow and menu navigation
- ✅ Farmer registration (name, location, ID verification)
- ✅ Farmer job preferences (work type, distance, hours)
- ✅ Farm owner registration (name, farm name, location)
- ✅ Job posting flow (complete 8-step process)
- ✅ Job matching and recommendations
- ✅ Job applications and match creation
- ✅ Menu navigation (farmer and owner menus)
- ✅ Preference updates

### SimpleFarmConnectBot Tests (`test_chatbot_simple.py`)
- ✅ Simplified welcome flow with emojis
- ✅ Simplified registration flows
- ✅ Emoji-rich preference setup
- ✅ Simplified job recommendations display
- ✅ Simplified menus
- ✅ Simple error messages
- ✅ Inheritance from FarmConnectBot

## Test Fixtures

Common fixtures available in `conftest.py`:
- `reset_environment`: Resets environment variables before each test
- `mock_twilio_env`: Mocks Twilio credentials

Test-specific fixtures:
- `temp_data_dir`: Creates temporary data directory
- `mock_data_store`: DataStore instance with temp directory
- `bot`: FarmConnectBot instance with mocked dependencies
- `simple_bot`: SimpleFarmConnectBot instance with mocked dependencies

## Writing New Tests

When adding new tests:

1. Create test classes grouped by functionality
2. Use descriptive test names: `test_<what_is_being_tested>`
3. Follow the Arrange-Act-Assert pattern
4. Use fixtures to reduce code duplication
5. Mock external dependencies (Twilio, AI matcher)
6. Clean up temporary resources

Example:
```python
def test_create_user_farmer(self, data_store):
    """Test creating a farmer user"""
    # Arrange
    phone = "whatsapp:+15555551234"

    # Act
    user = data_store.create_user(phone, 'farmer')

    # Assert
    assert user is not None
    assert user['type'] == 'farmer'
```

## Continuous Integration

These tests are designed to run in CI/CD pipelines. They:
- Use temporary directories (no filesystem pollution)
- Mock external services (no API calls)
- Run independently (no test interdependencies)
- Clean up resources automatically

## Coverage Goals

Target coverage: **>80%** for all modules

View coverage report:
```bash
pytest --cov=. --cov-report=html
open htmlcov/index.html
```
