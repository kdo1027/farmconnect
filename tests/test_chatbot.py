"""
Unit tests for FarmConnectBot class
Tests conversation flows, registration, job posting, and matching
"""
import pytest
import tempfile
import shutil
import os
from unittest.mock import Mock, patch, MagicMock
from chatbot import FarmConnectBot
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
def bot(mock_data_store):
    """Create a FarmConnectBot instance with mocked dependencies"""
    with patch('chatbot.DataStore', return_value=mock_data_store):
        bot = FarmConnectBot()
        bot.store = mock_data_store
        bot.twilio_client = None  # Disable Twilio for testing
        bot.ai_matcher = None  # Disable AI matching for testing
    return bot


class TestBotWelcomeFlow:
    """Test welcome and initial user interaction"""

    def test_new_user_shows_welcome_menu(self, bot):
        """Test that new users see welcome menu"""
        phone = "whatsapp:+15555551234"
        response = bot.handle_message(phone, "Hello")

        assert "Welcome to FarmConnect" in response
        assert "looking for farm work" in response
        assert "hiring workers" in response

    def test_welcome_menu_sets_conversation_state(self, bot):
        """Test that welcome menu sets awaiting_role_selection state"""
        phone = "whatsapp:+15555551234"
        bot.handle_message(phone, "Hello")

        state = bot.store.get_conversation_state(phone)
        assert state is not None
        assert state['state'] == 'awaiting_role_selection'


class TestFarmerRegistration:
    """Test farmer registration flow"""

    def test_select_farmer_role(self, bot):
        """Test selecting farmer role"""
        phone = "whatsapp:+15555551234"
        # Show welcome menu
        bot.handle_message(phone, "Hello")

        # Select farmer (option 1)
        response = bot.handle_message(phone, "1")

        assert "Let's get you registered" in response
        assert "What's your full name" in response

        user = bot.store.get_user(phone)
        assert user is not None
        assert user['type'] == 'farmer'

    def test_farmer_registration_name(self, bot):
        """Test farmer name input"""
        phone = "whatsapp:+15555551234"
        bot.store.create_user(phone, 'farmer')
        bot.store.set_conversation_state(phone, 'farmer_reg_name')

        response = bot.handle_message(phone, "John Doe")

        assert "John Doe" in response
        assert "location" in response.lower()

        user = bot.store.get_user(phone)
        assert user['profile']['name'] == 'John Doe'

    def test_farmer_registration_location(self, bot):
        """Test farmer location input"""
        phone = "whatsapp:+15555551234"
        bot.store.create_user(phone, 'farmer')
        bot.store.update_user_profile(phone, {'name': 'John Doe'})
        bot.store.set_conversation_state(phone, 'farmer_reg_location')

        response = bot.handle_message(phone, "Chapel Hill, NC")

        assert "ID" in response or "photo" in response
        user = bot.store.get_user(phone)
        assert user['profile']['location'] == 'Chapel Hill, NC'

    def test_farmer_id_upload(self, bot):
        """Test farmer ID photo upload"""
        phone = "whatsapp:+15555551234"
        bot.store.create_user(phone, 'farmer')
        bot.store.update_user_profile(phone, {'name': 'John Doe', 'location': 'Chapel Hill'})
        bot.store.set_conversation_state(phone, 'farmer_reg_id')

        media_url = "https://example.com/id_photo.jpg"
        response = bot.handle_message(phone, "", media_url=media_url)

        assert "ID received" in response
        assert "preferences" in response.lower() or "work type" in response.lower()

        user = bot.store.get_user(phone)
        assert user['profile']['id_verified'] == True
        assert user['profile']['id_photo_url'] == media_url

    def test_farmer_id_no_photo(self, bot):
        """Test farmer ID upload without photo"""
        phone = "whatsapp:+15555551234"
        bot.store.create_user(phone, 'farmer')
        bot.store.set_conversation_state(phone, 'farmer_reg_id')

        response = bot.handle_message(phone, "I uploaded it", media_url=None)

        assert "photo of your ID" in response


class TestFarmerPreferences:
    """Test farmer job preferences setup"""

    def test_work_type_preference_single(self, bot):
        """Test selecting single work type"""
        phone = "whatsapp:+15555551234"
        bot.store.create_user(phone, 'farmer')
        bot.store.set_conversation_state(phone, 'farmer_pref_work_type')

        response = bot.handle_message(phone, "1")  # Harvesting

        user = bot.store.get_user(phone)
        assert 'Harvesting' in user['profile']['work_types']

    def test_work_type_preference_multiple(self, bot):
        """Test selecting multiple work types"""
        phone = "whatsapp:+15555551234"
        bot.store.create_user(phone, 'farmer')
        bot.store.set_conversation_state(phone, 'farmer_pref_work_type')

        response = bot.handle_message(phone, "1,2,3")

        user = bot.store.get_user(phone)
        assert 'Harvesting' in user['profile']['work_types']
        assert 'Planting' in user['profile']['work_types']
        assert 'Irrigation' in user['profile']['work_types']

    def test_distance_preference(self, bot):
        """Test setting distance preference"""
        phone = "whatsapp:+15555551234"
        bot.store.create_user(phone, 'farmer')
        bot.store.update_user_profile(phone, {'work_types': 'Harvesting'})
        bot.store.set_conversation_state(phone, 'farmer_pref_location')

        response = bot.handle_message(phone, "2")  # 25 miles

        user = bot.store.get_user(phone)
        assert user['profile']['max_distance'] == 25

    def test_hours_preference(self, bot):
        """Test setting hours preference"""
        phone = "whatsapp:+15555551234"
        bot.store.create_user(phone, 'farmer')
        bot.store.update_user_profile(phone, {
            'work_types': 'Harvesting',
            'max_distance': 25
        })
        bot.store.set_conversation_state(phone, 'farmer_pref_hours')

        response = bot.handle_message(phone, "1")  # Full-time

        user = bot.store.get_user(phone)
        assert user['profile']['hours_preference'] == 'full-time'


class TestFarmOwnerRegistration:
    """Test farm owner registration flow"""

    def test_select_owner_role(self, bot):
        """Test selecting farm owner role"""
        phone = "whatsapp:+15555550001"
        bot.handle_message(phone, "Hello")

        response = bot.handle_message(phone, "2")  # Farm owner

        assert "farm owner" in response.lower()
        assert "name" in response.lower()

        user = bot.store.get_user(phone)
        assert user['type'] == 'farm_owner'

    def test_owner_registration_name(self, bot):
        """Test owner name input"""
        phone = "whatsapp:+15555550001"
        bot.store.create_user(phone, 'farm_owner')
        bot.store.set_conversation_state(phone, 'owner_reg_name')

        response = bot.handle_message(phone, "Sarah Johnson")

        assert "farm" in response.lower()
        user = bot.store.get_user(phone)
        assert user['profile']['name'] == 'Sarah Johnson'

    def test_owner_registration_farm_name(self, bot):
        """Test farm name input"""
        phone = "whatsapp:+15555550001"
        bot.store.create_user(phone, 'farm_owner')
        bot.store.update_user_profile(phone, {'name': 'Sarah Johnson'})
        bot.store.set_conversation_state(phone, 'owner_reg_farm_name')

        response = bot.handle_message(phone, "Sunny Acres Farm")

        assert "locat" in response.lower()  # Matches both "location" and "located"
        user = bot.store.get_user(phone)
        assert user['profile']['farm_name'] == 'Sunny Acres Farm'

    def test_owner_registration_complete(self, bot):
        """Test completing owner registration"""
        phone = "whatsapp:+15555550001"
        bot.store.create_user(phone, 'farm_owner')
        bot.store.update_user_profile(phone, {
            'name': 'Sarah Johnson',
            'farm_name': 'Sunny Acres Farm'
        })
        bot.store.set_conversation_state(phone, 'owner_reg_location')

        response = bot.handle_message(phone, "Sacramento, CA")

        assert "complete" in response.lower() or "welcome" in response.lower()
        user = bot.store.get_user(phone)
        assert user['registered'] == True
        assert user['profile']['location'] == 'Sacramento, CA'


class TestJobPosting:
    """Test job posting flow"""

    def test_start_job_posting(self, bot):
        """Test starting job posting"""
        phone = "whatsapp:+15555550001"
        bot.store.create_user(phone, 'farm_owner')
        bot.store.update_user(phone, {'registered': True})

        response = bot.start_job_posting(phone)

        assert "work" in response.lower()
        state = bot.store.get_conversation_state(phone)
        assert state['state'] == 'job_work_type'

    def test_job_posting_work_type(self, bot):
        """Test entering work type"""
        phone = "whatsapp:+15555550001"
        bot.store.create_user(phone, 'farm_owner')
        bot.store.set_conversation_state(phone, 'job_work_type', {})

        response = bot.handle_message(phone, "Tomato Harvest")

        assert "workers" in response.lower()
        state = bot.store.get_conversation_state(phone)
        assert state['data']['work_type'] == 'Tomato Harvest'

    def test_job_posting_complete_flow(self, bot):
        """Test complete job posting flow"""
        phone = "whatsapp:+15555550001"
        bot.store.create_user(phone, 'farm_owner')
        bot.store.update_user(phone, {'registered': True})
        bot.store.update_user_profile(phone, {
            'name': 'Sarah Johnson',
            'farm_name': 'Sunny Acres Farm'
        })

        # Start job posting
        bot.store.set_conversation_state(phone, 'job_work_type', {})
        bot.handle_message(phone, "Tomato Harvest")

        # Workers needed
        state = bot.store.get_conversation_state(phone)
        bot.handle_message(phone, "5")

        # Work hours
        state = bot.store.get_conversation_state(phone)
        bot.handle_message(phone, "6:00 AM - 2:00 PM")

        # Payment type
        state = bot.store.get_conversation_state(phone)
        bot.handle_message(phone, "1")  # Per hour

        # Payment amount
        state = bot.store.get_conversation_state(phone)
        bot.handle_message(phone, "18")

        # Location
        state = bot.store.get_conversation_state(phone)
        bot.handle_message(phone, "Green Valley Farm, Sacramento")

        # Transportation
        state = bot.store.get_conversation_state(phone)
        bot.handle_message(phone, "2")  # Not provided

        # Description
        state = bot.store.get_conversation_state(phone)
        response = bot.handle_message(phone, "skip")

        assert "posted" in response.lower() or "success" in response.lower()

        # Verify job was created
        jobs = bot.store.get_open_jobs()
        assert len(jobs) == 1
        assert jobs[0]['work_type'] == 'Tomato Harvest'


class TestJobMatching:
    """Test job matching and recommendations"""

    def test_job_recommendations_no_jobs(self, bot):
        """Test recommendations when no jobs available"""
        phone = "whatsapp:+15555551234"
        bot.store.create_user(phone, 'farmer')
        bot.store.update_user(phone, {'registered': True})
        bot.store.update_user_profile(phone, {
            'work_types': 'Harvesting',
            'max_distance': 25
        })

        response = bot.show_job_recommendations(phone)

        assert "no job" in response.lower() or "notify" in response.lower()

    def test_job_recommendations_with_matches(self, bot):
        """Test recommendations with matching jobs"""
        # Create farmer
        phone = "whatsapp:+15555551234"
        bot.store.create_user(phone, 'farmer')
        bot.store.update_user(phone, {'registered': True})
        bot.store.update_user_profile(phone, {
            'work_types': 'All types of work',  # Changed to match all jobs
            'max_distance': 50,
            'hours_preference': 'full-time'
        })

        # Create matching job
        job_data = {
            'work_type': 'Tomato Harvest',
            'workers_needed': 5,
            'work_hours': '6:00 AM - 2:00 PM',
            'payment_type': 'per day',
            'payment_amount': 150.00,
            'location': 'Green Valley Farm',
            'transportation': 'provided',
            'meeting_point': 'Town Square',
            'owner_phone': 'whatsapp:+15555550001',
            'owner_name': 'Sarah',
            'farm_name': 'Sunny Acres',
            'hours': 'full-time'
        }
        bot.store.create_job(job_data)

        response = bot.show_job_recommendations(phone)

        assert "found" in response.lower() or "job" in response.lower()
        assert "Tomato Harvest" in response

    def test_job_application(self, bot):
        """Test applying for a job"""
        # Create farmer
        farmer_phone = "whatsapp:+15555551234"
        bot.store.create_user(farmer_phone, 'farmer')
        bot.store.update_user(farmer_phone, {'registered': True})
        bot.store.update_user_profile(farmer_phone, {'name': 'John Doe'})

        # Create job
        job_data = {
            'work_type': 'Tomato Harvest',
            'pay_rate': 18.00,
            'location': 'Test Farm',
            'hours': 'full-time',
            'workers_needed': 5,
            'owner_phone': 'whatsapp:+15555550001'
        }
        job_id = bot.store.create_job(job_data)

        # Apply for job
        bot.store.set_conversation_state(farmer_phone, 'job_details_view', {
            'job_id': job_id,
            'all_jobs': [job_id]
        })

        response = bot.handle_message(farmer_phone, "1")  # Apply

        assert "application submitted" in response.lower() or "applied" in response.lower()

        # Verify match was created
        matches = bot.store.get_farmer_matches(farmer_phone)
        assert len(matches) == 1
        assert matches[0]['job_id'] == job_id


class TestMenus:
    """Test menu navigation"""

    def test_farmer_menu(self, bot):
        """Test farmer main menu"""
        phone = "whatsapp:+15555551234"
        bot.store.create_user(phone, 'farmer')
        bot.store.update_user(phone, {'registered': True})

        response = bot.show_farmer_menu(phone)

        assert "Farmer Menu" in response
        assert "Browse" in response or "jobs" in response.lower()
        assert "preferences" in response.lower()

    def test_owner_menu(self, bot):
        """Test owner main menu"""
        phone = "whatsapp:+15555550001"
        bot.store.create_user(phone, 'farm_owner')
        bot.store.update_user(phone, {'registered': True})

        response = bot.show_owner_menu(phone)

        assert "Owner Menu" in response or "Farm Owner" in response
        assert "Post" in response or "job" in response.lower()

    def test_registered_user_shows_menu(self, bot):
        """Test that registered users see main menu"""
        phone = "whatsapp:+15555551234"
        bot.store.create_user(phone, 'farmer')
        bot.store.update_user(phone, {'registered': True})

        response = bot.handle_message(phone, "menu")

        assert "Menu" in response


class TestUpdatePreferences:
    """Test updating farmer preferences"""

    def test_update_work_type(self, bot):
        """Test updating work type preferences"""
        phone = "whatsapp:+15555551234"
        bot.store.create_user(phone, 'farmer')
        bot.store.update_user(phone, {'registered': True})
        bot.store.update_user_profile(phone, {'work_types': 'Harvesting'})

        bot.store.set_conversation_state(phone, 'farmer_update_work_type')
        response = bot.handle_message(phone, "Planting, Irrigation")

        user = bot.store.get_user(phone)
        assert 'Planting' in user['profile']['work_types']

    def test_update_location(self, bot):
        """Test updating location"""
        phone = "whatsapp:+15555551234"
        bot.store.create_user(phone, 'farmer')
        bot.store.update_user(phone, {'registered': True})
        bot.store.update_user_profile(phone, {'location': 'Chapel Hill'})

        bot.store.set_conversation_state(phone, 'farmer_pref_actual_location')
        response = bot.handle_message(phone, "Durham, NC")

        user = bot.store.get_user(phone)
        assert user['profile']['location'] == 'Durham, NC'
