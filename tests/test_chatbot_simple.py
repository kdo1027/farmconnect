"""
Unit tests for SimpleFarmConnectBot class
Tests simplified conversation flows optimized for low-literacy users
"""
import pytest
import tempfile
import shutil
import os
from unittest.mock import patch
from chatbot_simple import SimpleFarmConnectBot
from data_store import DataStore


@pytest.fixture
def temp_data_dir():
    """Create a temporary data directory for testing"""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)


@pytest.fixture
def mock_data_store(temp_data_dir):
    """Create a mock DataStore with temporary directory"""
    store = DataStore()
    store.data_dir = temp_data_dir
    store.users_file = os.path.join(temp_data_dir, 'users.json')
    store.jobs_file = os.path.join(temp_data_dir, 'jobs.json')
    store.conversations_file = os.path.join(temp_data_dir, 'conversations.json')
    store.matches_file = os.path.join(temp_data_dir, 'matches.json')

    store._write_json(store.users_file, {})
    store._write_json(store.jobs_file, {})
    store._write_json(store.conversations_file, {})
    store._write_json(store.matches_file, {})

    return store


@pytest.fixture
def simple_bot(mock_data_store):
    """Create a SimpleFarmConnectBot instance with mocked dependencies"""
    with patch('chatbot.DataStore', return_value=mock_data_store):
        bot = SimpleFarmConnectBot()
        bot.store = mock_data_store
        bot.twilio_client = None
        bot.ai_matcher = None
    return bot


class TestSimpleBotWelcomeFlow:
    """Test simplified welcome flow"""

    def test_welcome_message_uses_emojis(self, simple_bot):
        """Test that welcome message uses emojis and minimal text"""
        phone = "whatsapp:+15555551234"
        response = simple_bot.handle_message(phone, "Hello")

        # Check for emojis
        assert "🌾" in response
        assert "👤" in response or "👷" in response or "🚜" in response
        # Check for simplified text
        assert "Who are you?" in response
        assert "Worker" in response or "Find Job" in response
        assert "Farm Owner" in response or "Hire" in response

    def test_welcome_menu_shows_simple_options(self, simple_bot):
        """Test welcome menu shows simple numbered options"""
        phone = "whatsapp:+15555551234"
        response = simple_bot.handle_message(phone, "Hello")

        assert "1️⃣" in response
        assert "2️⃣" in response
        assert "Send: 1 or 2" in response


class TestSimpleFarmerRegistration:
    """Test simplified farmer registration"""

    def test_farmer_registration_simple_prompts(self, simple_bot):
        """Test that registration uses simple prompts"""
        phone = "whatsapp:+15555551234"
        simple_bot.handle_message(phone, "Hello")
        response = simple_bot.handle_message(phone, "1")  # Select worker

        assert "Welcome Worker" in response
        assert "Your Name?" in response
        assert "📝" in response  # Progress emoji

    def test_farmer_name_simplified(self, simple_bot):
        """Test farmer name input with simplified response"""
        phone = "whatsapp:+15555551234"
        simple_bot.store.create_user(phone, 'farmer')
        simple_bot.store.set_conversation_state(phone, 'farmer_reg_name')

        response = simple_bot.handle_message(phone, "John")

        assert "Hi John" in response
        assert "Your City?" in response
        assert "📍" in response

    def test_farmer_location_simplified(self, simple_bot):
        """Test location input with simplified response"""
        phone = "whatsapp:+15555551234"
        simple_bot.store.create_user(phone, 'farmer')
        simple_bot.store.update_user_profile(phone, {'name': 'John'})
        simple_bot.store.set_conversation_state(phone, 'farmer_reg_location')

        response = simple_bot.handle_message(phone, "Chapel Hill")

        assert "Send ID Photo" in response
        assert "📸" in response

    def test_farmer_id_simplified_error(self, simple_bot):
        """Test ID upload error with simple message"""
        phone = "whatsapp:+15555551234"
        simple_bot.store.create_user(phone, 'farmer')
        simple_bot.store.set_conversation_state(phone, 'farmer_reg_id')

        response = simple_bot.handle_message(phone, "text", media_url=None)

        assert "No photo" in response or "Please send photo" in response
        assert "❌" in response


class TestSimpleFarmerPreferences:
    """Test simplified preference setup"""

    def test_work_type_with_emoji_options(self, simple_bot):
        """Test work type selection shows emoji options"""
        phone = "whatsapp:+15555551234"
        simple_bot.store.create_user(phone, 'farmer')
        simple_bot.store.update_user_profile(phone, {
            'id_verified': True,
            'id_photo_url': 'http://example.com/id.jpg'
        })
        simple_bot.store.set_conversation_state(phone, 'farmer_reg_id')

        response = simple_bot.handle_message(phone, "", media_url="http://example.com/id.jpg")

        # Check for emoji work types
        assert "🌾" in response or "🌱" in response or "💧" in response
        assert "Harvest" in response
        assert "Plant" in response

    def test_distance_with_emoji_indicators(self, simple_bot):
        """Test distance preference shows emoji indicators"""
        phone = "whatsapp:+15555551234"
        simple_bot.store.create_user(phone, 'farmer')
        simple_bot.store.update_user_profile(phone, {'work_types': 'Harvesting'})
        simple_bot.store.set_conversation_state(phone, 'farmer_pref_work_type')

        # Trigger work type which leads to distance preference
        response = simple_bot.handle_message(phone, "1")  # Select harvesting

        # This should show distance preference prompt
        assert "📍" in response
        assert "10 miles" in response
        assert "25 miles" in response

    def test_hours_with_visual_indicators(self, simple_bot):
        """Test hours preference shows visual time indicators"""
        phone = "whatsapp:+15555551234"
        simple_bot.store.create_user(phone, 'farmer')
        simple_bot.store.update_user_profile(phone, {
            'work_types': 'Harvesting',
            'max_distance': 25
        })
        simple_bot.store.set_conversation_state(phone, 'farmer_pref_hours')

        # Trigger the hours preference prompt
        response = simple_bot.handle_hours(phone, "")

        # Should show error first
        assert "Wrong number" in response or "Send: 1, 2, or 3" in response


class TestSimpleOwnerRegistration:
    """Test simplified owner registration"""

    def test_owner_registration_simple(self, simple_bot):
        """Test owner registration uses simple language"""
        phone = "whatsapp:+15555550001"
        simple_bot.handle_message(phone, "Hello")
        response = simple_bot.handle_message(phone, "2")  # Farm owner

        assert "Welcome Farm Owner" in response
        assert "Your Name?" in response
        assert "📝" in response

    def test_owner_farm_name_simple(self, simple_bot):
        """Test farm name prompt is simple"""
        phone = "whatsapp:+15555550001"
        simple_bot.store.create_user(phone, 'farm_owner')
        simple_bot.store.set_conversation_state(phone, 'owner_reg_name')

        response = simple_bot.handle_message(phone, "Sarah")

        assert "Farm Name?" in response
        assert "🚜" in response


class TestSimpleJobRecommendations:
    """Test simplified job recommendations display"""

    def test_job_list_simplified_display(self, simple_bot):
        """Test job recommendations use simplified display"""
        # Create farmer
        phone = "whatsapp:+15555551234"
        simple_bot.store.create_user(phone, 'farmer')
        simple_bot.store.update_user(phone, {'registered': True})
        simple_bot.store.update_user_profile(phone, {
            'work_types': 'All types of work',
            'max_distance': 50
        })

        # Create job
        job_data = {
            'work_type': 'Tomato Harvest',
            'workers_needed': 5,
            'payment_type': 'per day',
            'payment_amount': 150.00,
            'location': 'Green Valley',
            'farm_name': 'Sunny Farm',
            'hours': 'full-time',
            'owner_phone': 'whatsapp:+15555550001'
        }
        simple_bot.store.create_job(job_data)

        response = simple_bot.show_job_recommendations(phone)

        # Check simplified format
        assert "Found" in response
        assert "Job" in response
        assert "💰" in response  # Pay emoji
        assert "📍" in response  # Location emoji
        assert "$150.0/day" in response or "$150" in response

    def test_job_details_simplified(self, simple_bot):
        """Test job details view is simplified"""
        phone = "whatsapp:+15555551234"
        simple_bot.store.create_user(phone, 'farmer')

        job_data = {
            'work_type': 'Tomato Harvest',
            'workers_needed': 5,
            'payment_type': 'per day',
            'payment_amount': 150.00,
            'location': 'Green Valley',
            'farm_name': 'Sunny Farm',
            'work_hours': '6 AM - 2 PM',
            'transportation': 'provided',
            'meeting_point': 'Town Square',
            'description': 'Pick tomatoes',
            'hours': 'full-time',
            'owner_phone': 'whatsapp:+15555550001'
        }
        job_id = simple_bot.store.create_job(job_data)

        simple_bot.store.set_conversation_state(phone, 'selecting_from_recommendations', {
            'jobs': [job_id]
        })

        response = simple_bot.handle_message(phone, "1")

        # Check for simplified display elements
        assert "Job Details" in response
        assert "Apply for this job?" in response
        assert "✅" in response
        assert "⬅️" in response or "Back" in response


class TestSimpleMenus:
    """Test simplified menu displays"""

    def test_farmer_menu_simple(self, simple_bot):
        """Test farmer menu uses simple language and emojis"""
        phone = "whatsapp:+15555551234"
        simple_bot.store.create_user(phone, 'farmer')
        simple_bot.store.update_user(phone, {'registered': True})

        response = simple_bot.show_farmer_menu(phone)

        assert "Worker Menu" in response
        assert "💼" in response  # Job emoji
        assert "⚙️" in response  # Settings emoji
        assert "Find Jobs" in response
        assert "Send number" in response

    def test_owner_menu_simple(self, simple_bot):
        """Test owner menu uses simple language"""
        phone = "whatsapp:+15555550001"
        simple_bot.store.create_user(phone, 'farm_owner')
        simple_bot.store.update_user(phone, {'registered': True})

        response = simple_bot.show_owner_menu(phone)

        assert "Owner Menu" in response
        assert "➕" in response or "Post Job" in response
        assert "📋" in response


class TestSimpleErrorMessages:
    """Test simplified error messages"""

    def test_invalid_work_type_simple_error(self, simple_bot):
        """Test invalid work type shows simple error"""
        phone = "whatsapp:+15555551234"
        simple_bot.store.create_user(phone, 'farmer')
        simple_bot.store.set_conversation_state(phone, 'farmer_pref_work_type')

        response = simple_bot.handle_message(phone, "invalid")

        assert "Wrong number" in response or "❌" in response

    def test_invalid_distance_simple_error(self, simple_bot):
        """Test invalid distance shows simple error"""
        phone = "whatsapp:+15555551234"
        simple_bot.store.create_user(phone, 'farmer')
        simple_bot.store.set_conversation_state(phone, 'farmer_pref_location')

        response = simple_bot.handle_message(phone, "99")

        assert "Wrong number" in response or "❌" in response


class TestSimpleJobApplication:
    """Test simplified job application flow"""

    def test_application_confirmation_simple(self, simple_bot):
        """Test application confirmation uses simple language"""
        phone = "whatsapp:+15555551234"
        simple_bot.store.create_user(phone, 'farmer')
        simple_bot.store.update_user(phone, {'registered': True})
        simple_bot.store.update_user_profile(phone, {'name': 'John'})

        job_data = {
            'work_type': 'Tomato Harvest',
            'workers_needed': 5,
            'payment_type': 'per day',
            'payment_amount': 150.00,
            'location': 'Green Valley',
            'farm_name': 'Sunny Farm',
            'hours': 'full-time',
            'owner_phone': 'whatsapp:+15555550001'
        }
        job_id = simple_bot.store.create_job(job_data)

        simple_bot.store.set_conversation_state(phone, 'job_details_view', {
            'job_id': job_id,
            'all_jobs': [job_id]
        })

        response = simple_bot.handle_message(phone, "1")

        assert "Applied" in response
        assert "✅" in response
        assert "Owner will contact you" in response


class TestSimpleInheritance:
    """Test that SimpleFarmConnectBot inherits from FarmConnectBot"""

    def test_inherits_core_functionality(self, simple_bot):
        """Test that simple bot inherits core bot functionality"""
        phone = "whatsapp:+15555551234"

        # Should still create users
        simple_bot.store.create_user(phone, 'farmer')
        user = simple_bot.store.get_user(phone)
        assert user is not None

        # Should still handle state
        simple_bot.store.set_conversation_state(phone, 'test_state')
        state = simple_bot.store.get_conversation_state(phone)
        assert state['state'] == 'test_state'

    def test_overrides_display_methods(self, simple_bot):
        """Test that display methods are overridden for simplicity"""
        phone = "whatsapp:+15555551234"

        # Simple bot should use simpler welcome
        response = simple_bot.show_welcome_menu(phone)
        assert "Who are you?" in response  # Simpler than base class

        # Verify it's different from base class
        from chatbot import FarmConnectBot
        base_bot = FarmConnectBot()
        base_bot.store = simple_bot.store
        base_response = base_bot.show_welcome_menu(phone)

        assert response != base_response
        assert len(response) < len(base_response)  # Simplified version should be shorter
