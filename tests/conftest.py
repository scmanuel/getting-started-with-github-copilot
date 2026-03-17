"""Pytest configuration and fixtures for API tests."""

import pytest
from copy import deepcopy
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def test_client():
    """Create a TestClient instance for testing the FastAPI app."""
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    """Reset activities to a clean state before each test."""
    # Store the original activities
    original_activities = deepcopy(activities)
    
    yield
    
    # Restore original activities after test
    activities.clear()
    activities.update(original_activities)


# Test data fixtures for commonly used values
@pytest.fixture
def valid_email():
    """A valid test email that is not initially registered."""
    return "newstudent@mergington.edu"


@pytest.fixture
def existing_participant():
    """An email that is already registered for Chess Club."""
    return "michael@mergington.edu"


@pytest.fixture
def valid_activity():
    """A valid activity name that exists in the system."""
    return "Chess Club"


@pytest.fixture
def invalid_activity():
    """An activity name that does not exist."""
    return "Nonexistent Club"
