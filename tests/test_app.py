"""Tests for the main API endpoints."""

import pytest


class TestGetActivities:
    """Tests for GET /activities endpoint."""

    def test_get_activities_success(self, test_client):
        """Test successful retrieval of all activities."""
        response = test_client.get("/activities")
        
        assert response.status_code == 200
        activities = response.json()
        
        # Verify it returns a dictionary of activities
        assert isinstance(activities, dict)
        assert len(activities) > 0

    def test_get_activities_contains_required_fields(self, test_client):
        """Test that each activity contains all required fields."""
        response = test_client.get("/activities")
        activities = response.json()
        
        required_fields = ["description", "schedule", "max_participants", "participants"]
        
        for activity_name, activity_data in activities.items():
            for field in required_fields:
                assert field in activity_data, f"Missing field '{field}' in activity '{activity_name}'"
                assert activity_data[field] is not None

    def test_get_activities_participants_is_list(self, test_client):
        """Test that participants field is a list."""
        response = test_client.get("/activities")
        activities = response.json()
        
        for activity_name, activity_data in activities.items():
            assert isinstance(activity_data["participants"], list), \
                f"Participants should be a list for activity '{activity_name}'"

    def test_get_activities_max_participants_is_integer(self, test_client):
        """Test that max_participants field is an integer."""
        response = test_client.get("/activities")
        activities = response.json()
        
        for activity_name, activity_data in activities.items():
            assert isinstance(activity_data["max_participants"], int), \
                f"max_participants should be an integer for activity '{activity_name}'"
            assert activity_data["max_participants"] > 0

    def test_get_activities_known_activity_exists(self, test_client):
        """Test that known activities are present in response."""
        response = test_client.get("/activities")
        activities = response.json()
        
        # Chess Club should exist (from initial data)
        assert "Chess Club" in activities
        assert "Programming Class" in activities
