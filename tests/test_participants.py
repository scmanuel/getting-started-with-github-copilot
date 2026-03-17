"""Tests for the participant removal endpoint."""

import pytest


class TestRemoveParticipant:
    """Tests for DELETE /activities/{activity_name}/participants/{email} endpoint."""

    def test_remove_participant_success(self, test_client, existing_participant, valid_activity):
        """Test successful removal of a participant from an activity."""
        # Verify participant exists first
        activities_before = test_client.get("/activities").json()
        assert existing_participant in activities_before[valid_activity]["participants"]
        
        # Remove participant
        response = test_client.delete(
            f"/activities/{valid_activity}/participants/{existing_participant}"
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert existing_participant in data["message"]
        assert valid_activity in data["message"]

    def test_remove_participant_actually_removes(self, test_client, existing_participant, valid_activity):
        """Test that removal actually removes the participant from the activity."""
        # Get initial count
        activities_before = test_client.get("/activities").json()
        initial_count = len(activities_before[valid_activity]["participants"])
        
        # Remove participant
        test_client.delete(
            f"/activities/{valid_activity}/participants/{existing_participant}"
        )
        
        # Verify participant is gone
        activities_after = test_client.get("/activities").json()
        assert existing_participant not in activities_after[valid_activity]["participants"]
        assert len(activities_after[valid_activity]["participants"]) == initial_count - 1

    def test_remove_participant_activity_not_found(self, test_client, existing_participant, invalid_activity):
        """Test removal from a non-existent activity returns 404."""
        response = test_client.delete(
            f"/activities/{invalid_activity}/participants/{existing_participant}"
        )
        
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert "Activity not found" in data["detail"]

    def test_remove_participant_not_found(self, test_client, valid_email, valid_activity):
        """Test removal of a non-existent participant returns 404."""
        response = test_client.delete(
            f"/activities/{valid_activity}/participants/{valid_email}"
        )
        
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert "Participant not found" in data["detail"]

    def test_remove_participant_then_re_register(self, test_client, valid_email):
        """Test that a student can re-register after being removed."""
        activity = "Chess Club"
        
        # Sign up
        test_client.post(
            f"/activities/{activity}/signup",
            params={"email": valid_email}
        )
        
        # Remove
        test_client.delete(
            f"/activities/{activity}/participants/{valid_email}"
        )
        
        # Sign up again - should succeed
        response = test_client.post(
            f"/activities/{activity}/signup",
            params={"email": valid_email}
        )
        
        assert response.status_code == 200
        activities = test_client.get("/activities").json()
        assert valid_email in activities[activity]["participants"]

    def test_remove_one_participant_others_remain(self, test_client, valid_activity):
        """Test that removing one participant doesn't affect others."""
        email1 = "student1@mergington.edu"
        email2 = "student2@mergington.edu"
        
        # Sign up both
        test_client.post(
            f"/activities/{valid_activity}/signup",
            params={"email": email1}
        )
        test_client.post(
            f"/activities/{valid_activity}/signup",
            params={"email": email2}
        )
        
        # Remove one
        test_client.delete(
            f"/activities/{valid_activity}/participants/{email1}"
        )
        
        # Verify the other is still there
        activities = test_client.get("/activities").json()
        assert email1 not in activities[valid_activity]["participants"]
        assert email2 in activities[valid_activity]["participants"]

    def test_remove_participant_with_special_characters_email(self, test_client, valid_activity):
        """Test removal of a participant with special characters in email."""
        special_email = "student+test@mergington.edu"
        
        # Sign up
        test_client.post(
            f"/activities/{valid_activity}/signup",
            params={"email": special_email}
        )
        
        # Remove
        response = test_client.delete(
            f"/activities/{valid_activity}/participants/{special_email}"
        )
        
        assert response.status_code == 200
        activities = test_client.get("/activities").json()
        assert special_email not in activities[valid_activity]["participants"]
