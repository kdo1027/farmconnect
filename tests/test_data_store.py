"""
Unit tests for DataStore class
Tests data persistence, user management, job postings, and matching
"""
import pytest
import json
import os
import tempfile
import shutil
from datetime import datetime
from data_store import DataStore


@pytest.fixture
def temp_data_dir():
    """Create a temporary data directory for testing"""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    # Cleanup after tests
    shutil.rmtree(temp_dir)


@pytest.fixture
def data_store(temp_data_dir):
    """Create a DataStore instance with temporary directory"""
    store = DataStore()
    # Override file paths to use temp directory
    store.data_dir = temp_data_dir
    store.users_file = os.path.join(temp_data_dir, 'users.json')
    store.jobs_file = os.path.join(temp_data_dir, 'jobs.json')
    store.conversations_file = os.path.join(temp_data_dir, 'conversations.json')
    store.matches_file = os.path.join(temp_data_dir, 'matches.json')

    # Initialize empty data files
    store._write_json(store.users_file, {})
    store._write_json(store.jobs_file, {})
    store._write_json(store.conversations_file, {})
    store._write_json(store.matches_file, {})

    return store


class TestDataStoreUserManagement:
    """Test user creation and management"""

    def test_create_user_farmer(self, data_store):
        """Test creating a farmer user"""
        phone = "whatsapp:+15555551234"
        user = data_store.create_user(phone, 'farmer')

        assert user is not None
        assert user['phone'] == phone
        assert user['type'] == 'farmer'
        assert user['registered'] == False
        assert 'created_at' in user
        assert 'profile' in user

    def test_create_user_farm_owner(self, data_store):
        """Test creating a farm owner user"""
        phone = "whatsapp:+15555551234"
        user = data_store.create_user(phone, 'farm_owner')

        assert user is not None
        assert user['phone'] == phone
        assert user['type'] == 'farm_owner'
        assert user['registered'] == False

    def test_get_user_exists(self, data_store):
        """Test retrieving an existing user"""
        phone = "whatsapp:+15555551234"
        data_store.create_user(phone, 'farmer')

        user = data_store.get_user(phone)
        assert user is not None
        assert user['phone'] == phone

    def test_get_user_not_exists(self, data_store):
        """Test retrieving a non-existent user"""
        user = data_store.get_user("whatsapp:+19999999999")
        assert user is None

    def test_update_user(self, data_store):
        """Test updating user data"""
        phone = "whatsapp:+15555551234"
        data_store.create_user(phone, 'farmer')

        data_store.update_user(phone, {'registered': True})
        user = data_store.get_user(phone)

        assert user['registered'] == True

    def test_update_user_profile(self, data_store):
        """Test updating user profile"""
        phone = "whatsapp:+15555551234"
        data_store.create_user(phone, 'farmer')

        profile_data = {
            'name': 'John Doe',
            'location': 'Chapel Hill, NC',
            'work_types': 'Harvesting, Planting'
        }
        data_store.update_user_profile(phone, profile_data)

        user = data_store.get_user(phone)
        assert user['profile']['name'] == 'John Doe'
        assert user['profile']['location'] == 'Chapel Hill, NC'
        assert user['profile']['work_types'] == 'Harvesting, Planting'


class TestDataStoreConversationState:
    """Test conversation state management"""

    def test_set_conversation_state_simple(self, data_store):
        """Test setting a simple conversation state"""
        phone = "whatsapp:+15555551234"
        data_store.set_conversation_state(phone, 'awaiting_role_selection')

        state = data_store.get_conversation_state(phone)
        assert state is not None
        assert state['state'] == 'awaiting_role_selection'
        assert state.get('data') == {}

    def test_set_conversation_state_with_data(self, data_store):
        """Test setting conversation state with data"""
        phone = "whatsapp:+15555551234"
        state_data = {'job_id': 'JOB_123', 'step': 1}
        data_store.set_conversation_state(phone, 'job_posting', state_data)

        state = data_store.get_conversation_state(phone)
        assert state['state'] == 'job_posting'
        assert state['data']['job_id'] == 'JOB_123'
        assert state['data']['step'] == 1

    def test_clear_conversation_state(self, data_store):
        """Test clearing conversation state"""
        phone = "whatsapp:+15555551234"
        data_store.set_conversation_state(phone, 'test_state')
        data_store.clear_conversation_state(phone)

        state = data_store.get_conversation_state(phone)
        assert state is None

    def test_get_conversation_state_not_exists(self, data_store):
        """Test getting non-existent conversation state"""
        state = data_store.get_conversation_state("whatsapp:+19999999999")
        assert state is None


class TestDataStoreJobManagement:
    """Test job creation and management"""

    def test_create_job_basic(self, data_store):
        """Test creating a basic job posting"""
        job_data = {
            'work_type': 'Tomato Harvest',
            'pay_rate': 18.00,
            'location': 'Chapel Hill, NC',
            'hours': 'full-time',
            'workers_needed': 5,
            'owner_phone': 'whatsapp:+15555550001',
            'owner_name': 'Farm Owner',
            'farm_name': 'Test Farm'
        }

        job_id = data_store.create_job(job_data)

        assert job_id is not None
        assert job_id.startswith('JOB_')

        job = data_store.get_job(job_id)
        assert job is not None
        assert job['work_type'] == 'Tomato Harvest'
        assert job['pay_rate'] == 18.00
        assert job['status'] == 'open'

    def test_create_job_detailed_format(self, data_store):
        """Test creating job with detailed payment format"""
        job_data = {
            'work_type': 'Strawberry Picking',
            'workers_needed': 8,
            'work_hours': '5:00 AM - 12:00 PM',
            'payment_type': 'per day',
            'payment_amount': 120.00,
            'location': 'Berry Farm, CA',
            'transportation': 'provided',
            'meeting_point': 'Town Square',
            'owner_phone': 'whatsapp:+15555550001',
            'owner_name': 'Farm Owner',
            'farm_name': 'Berry Farm'
        }

        job_id = data_store.create_job(job_data)
        job = data_store.get_job(job_id)

        assert job['payment_type'] == 'per day'
        assert job['payment_amount'] == 120.00
        assert job['transportation'] == 'provided'

    def test_get_job_not_exists(self, data_store):
        """Test getting non-existent job"""
        job = data_store.get_job('JOB_NONEXISTENT')
        assert job is None

    def test_update_job_status(self, data_store):
        """Test updating job status"""
        job_data = {
            'work_type': 'Test Job',
            'pay_rate': 15.00,
            'location': 'Test Location',
            'hours': 'full-time',
            'workers_needed': 3,
            'owner_phone': 'whatsapp:+15555550001'
        }

        job_id = data_store.create_job(job_data)
        data_store.update_job_status(job_id, 'filled')

        job = data_store.get_job(job_id)
        assert job['status'] == 'filled'

    def test_get_open_jobs(self, data_store):
        """Test retrieving only open jobs"""
        # Create open job
        job_data1 = {
            'work_type': 'Open Job',
            'pay_rate': 18.00,
            'location': 'Location 1',
            'hours': 'full-time',
            'workers_needed': 5,
            'owner_phone': 'whatsapp:+15555550001'
        }
        job_id1 = data_store.create_job(job_data1)

        # Create and close another job
        job_data2 = {
            'work_type': 'Closed Job',
            'pay_rate': 20.00,
            'location': 'Location 2',
            'hours': 'part-time',
            'workers_needed': 3,
            'owner_phone': 'whatsapp:+15555550001'
        }
        job_id2 = data_store.create_job(job_data2)
        data_store.update_job_status(job_id2, 'filled')

        open_jobs = data_store.get_open_jobs()

        assert len(open_jobs) == 1
        assert open_jobs[0]['job_id'] == job_id1
        assert open_jobs[0]['status'] == 'open'


class TestDataStoreMatching:
    """Test job matching functionality"""

    def test_create_match(self, data_store):
        """Test creating a job match"""
        # Create a job first
        job_data = {
            'work_type': 'Test Job',
            'pay_rate': 18.00,
            'location': 'Test Location',
            'hours': 'full-time',
            'workers_needed': 5,
            'owner_phone': 'whatsapp:+15555550001'
        }
        job_id = data_store.create_job(job_data)

        # Create a match
        farmer_phone = 'whatsapp:+15555551234'
        match_id = data_store.create_match(job_id, farmer_phone, 'accepted')

        assert match_id is not None
        assert match_id.startswith('MATCH_')

    def test_get_job_matches(self, data_store):
        """Test retrieving matches for a job"""
        # Create job
        job_data = {
            'work_type': 'Test Job',
            'pay_rate': 18.00,
            'location': 'Test Location',
            'hours': 'full-time',
            'workers_needed': 5,
            'owner_phone': 'whatsapp:+15555550001'
        }
        job_id = data_store.create_job(job_data)

        # Create multiple matches
        data_store.create_match(job_id, 'whatsapp:+15555551234', 'accepted')
        data_store.create_match(job_id, 'whatsapp:+15555555678', 'accepted')

        matches = data_store.get_job_matches(job_id)

        assert len(matches) == 2
        assert all(m['job_id'] == job_id for m in matches)

    def test_get_farmer_matches(self, data_store):
        """Test retrieving matches for a farmer"""
        farmer_phone = 'whatsapp:+15555551234'

        # Create jobs and matches
        for i in range(3):
            job_data = {
                'work_type': f'Job {i}',
                'pay_rate': 15.00 + i,
                'location': 'Test Location',
                'hours': 'full-time',
                'workers_needed': 5,
                'owner_phone': 'whatsapp:+15555550001'
            }
            job_id = data_store.create_job(job_data)
            data_store.create_match(job_id, farmer_phone, 'accepted')

        matches = data_store.get_farmer_matches(farmer_phone)

        assert len(matches) == 3
        assert all(m['farmer_phone'] == farmer_phone for m in matches)


class TestDataStorePersistence:
    """Test data persistence across instances"""

    def test_data_persists_across_instances(self, temp_data_dir):
        """Test that data persists when creating new DataStore instance"""
        # Create first instance and add data
        store1 = DataStore()
        store1.data_dir = temp_data_dir
        store1.users_file = os.path.join(temp_data_dir, 'users.json')
        store1.jobs_file = os.path.join(temp_data_dir, 'jobs.json')
        store1.conversations_file = os.path.join(temp_data_dir, 'conversations.json')
        store1.matches_file = os.path.join(temp_data_dir, 'matches.json')

        store1._write_json(store1.users_file, {})
        store1._write_json(store1.jobs_file, {})
        store1._write_json(store1.conversations_file, {})
        store1._write_json(store1.matches_file, {})

        phone = "whatsapp:+15555551234"
        store1.create_user(phone, 'farmer')
        store1.update_user_profile(phone, {'name': 'Test User'})

        # Create second instance with same paths
        store2 = DataStore()
        store2.data_dir = temp_data_dir
        store2.users_file = os.path.join(temp_data_dir, 'users.json')
        store2.jobs_file = os.path.join(temp_data_dir, 'jobs.json')
        store2.conversations_file = os.path.join(temp_data_dir, 'conversations.json')
        store2.matches_file = os.path.join(temp_data_dir, 'matches.json')

        # Verify data persisted
        user = store2.get_user(phone)
        assert user is not None
        assert user['profile']['name'] == 'Test User'
