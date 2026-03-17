"""Tests for the signup endpoint."""

import pytest


class TestSignup:
    """Tests for POST /activities/{activity_name}/signup endpoint."""

    def test_signup_success(self, test_client, valid_email, valid_activity):
        """Test successful signup for an activity."""
        response = test_client.post(
            f"/activities/{valid_activity}/signup",
            params={"email": valid_email}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert valid_email in data["message"]
        assert valid_activity in data["message"]

    def test_signup_adds_participant_to_activity(self, test_client, valid_email, valid_activity):
        """Test that signup actually adds the participant to the activity."""
        # Get initial state
        activities_before = test_client.get("/activities").json()
        initial_count = len(activities_before[valid_activity]["participants"])
        
        # Sign up
        test_client.post(
            f"/activities/{valid_activity}/signup",
            params={"email": valid_email}
        )
        
        # Verify participant was added
        activities_after = test_client.get("/activities").json()
        assert valid_email in activities_after[valid_activity]["participants"]
        assert len(activities_after[valid_activity]["participants"]) == initial_count + 1

    def test_signup_activity_not_found(self, test_client, valid_email, invalid_activity):
        """Test signup for a non-existent activity returns 404."""
        response = test_client.post(
            f"/activities/{invalid_activity}/signup",
            params={"email": valid_email}
        )
        
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert "Activity not found" in data["detail"]

    def test_signup_duplicate_registration_blocked(self, test_client, existing_participant, valid_activity):
        """Test that a student cannot register twice for the same activity."""
        response = test_client.post(
            f"/activities/{valid_activity}/signup",
            params={"email": existing_participant}
        )
        
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
        assert "already signed up" in data["detail"].lower()

    def test_signup_multiple_students_same_activity(self, test_client, valid_activity):
        """Test that multiple different students can sign up for the same activity."""
        email1 = "student1@mergington.edu"
        email2 = "student2@mergington.edu"
        
        # Both should succeed
        response1 = test_client.post(
            f"/activities/{valid_activity}/signup",
            params={"email": email1}
        )
        response2 = test_client.post(
            f"/activities/{valid_activity}/signup",
            params={"email": email2}
        )
        
        assert response1.status_code == 200
        assert response2.status_code == 200
        
        # Verify both are in the activity
        activities = test_client.get("/activities").json()
        assert email1 in activities[valid_activity]["participants"]
        assert email2 in activities[valid_activity]["participants"]

    def test_signup_same_student_different_activities(self, test_client, valid_email):
        """Test that a student can sign up for multiple different activities."""
        activity1 = "Chess Club"
        activity2 = "Programming Class"
        
        # Sign up for both activities
        response1 = test_client.post(
            f"/activities/{activity1}/signup",
            params={"email": valid_email}
        )
        response2 = test_client.post(
            f"/activities/{activity2}/signup",
            params={"email": valid_email}
        )
        
        assert response1.status_code == 200
        assert response2.status_code == 200
        
        # Verify student is in both activities
        activities = test_client.get("/activities").json()
        assert valid_email in activities[activity1]["participants"]
        assert valid_email in activities[activity2]["participants"]

    def test_signup_with_special_characters_email(self, test_client, valid_activity):
        """Test signup with an email containing special characters."""
        special_email = "student+test@mergington.edu"
        
        response = test_client.post(
            f"/activities/{valid_activity}/signup",
            params={"email": special_email}
        )
        
        assert response.status_code == 200
        activities = test_client.get("/activities").json()
        assert special_email in activities[valid_activity]["participants"]
