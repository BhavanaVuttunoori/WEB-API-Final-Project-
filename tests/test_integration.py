"""Integration tests for API endpoints"""
import pytest
from fastapi import status


class TestAuthEndpoints:
    """Test authentication endpoints"""

    def test_register_user(self, client, test_user_data):
        """Test user registration"""
        response = client.post("/api/auth/register", json=test_user_data)
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["username"] == test_user_data["username"]
        assert data["email"] == test_user_data["email"]
        assert "id" in data

    def test_register_duplicate_username(self, client, test_user_data):
        """Test registering with duplicate username"""
        client.post("/api/auth/register", json=test_user_data)
        response = client.post("/api/auth/register", json=test_user_data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "already registered" in response.json()["detail"]

    def test_register_duplicate_email(self, client, test_user_data):
        """Test registering with duplicate email"""
        client.post("/api/auth/register", json=test_user_data)
        different_user = test_user_data.copy()
        different_user["username"] = "different_user"
        response = client.post("/api/auth/register", json=different_user)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_login_success(self, client, test_user_data):
        """Test successful login"""
        client.post("/api/auth/register", json=test_user_data)
        response = client.post("/api/auth/login", json={
            "username": test_user_data["username"],
            "password": test_user_data["password"]
        })
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    def test_login_wrong_password(self, client, test_user_data):
        """Test login with wrong password"""
        client.post("/api/auth/register", json=test_user_data)
        response = client.post("/api/auth/login", json={
            "username": test_user_data["username"],
            "password": "wrongpassword"
        })
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_login_nonexistent_user(self, client):
        """Test login with nonexistent user"""
        response = client.post("/api/auth/login", json={
            "username": "nonexistent",
            "password": "password"
        })
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


class TestCalculationEndpoints:
    """Test calculation endpoints"""

    def test_create_calculation(self, authenticated_client):
        """Test creating a calculation"""
        response = authenticated_client.post("/api/calculations/", json={
            "operation": "add",
            "operand1": 5,
            "operand2": 3
        })
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["operation"] == "add"
        assert data["operand1"] == 5
        assert data["operand2"] == 3
        assert data["result"] == 8

    def test_create_calculation_unauthorized(self, client):
        """Test creating calculation without authentication"""
        response = client.post("/api/calculations/", json={
            "operation": "add",
            "operand1": 5,
            "operand2": 3
        })
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_calculation_division_by_zero(self, authenticated_client):
        """Test division by zero validation"""
        response = authenticated_client.post("/api/calculations/", json={
            "operation": "divide",
            "operand1": 10,
            "operand2": 0
        })
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_list_calculations(self, authenticated_client):
        """Test listing calculations"""
        # Create some calculations
        authenticated_client.post("/api/calculations/", json={
            "operation": "add",
            "operand1": 5,
            "operand2": 3
        })
        authenticated_client.post("/api/calculations/", json={
            "operation": "multiply",
            "operand1": 4,
            "operand2": 6
        })

        response = authenticated_client.get("/api/calculations/")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 2

    def test_get_calculation_by_id(self, authenticated_client):
        """Test getting specific calculation"""
        create_response = authenticated_client.post("/api/calculations/", json={
            "operation": "add",
            "operand1": 5,
            "operand2": 3
        })
        calc_id = create_response.json()["id"]

        response = authenticated_client.get(f"/api/calculations/{calc_id}")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == calc_id
        assert data["result"] == 8

    def test_get_nonexistent_calculation(self, authenticated_client):
        """Test getting nonexistent calculation"""
        response = authenticated_client.get("/api/calculations/9999")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_update_calculation(self, authenticated_client):
        """Test updating a calculation"""
        create_response = authenticated_client.post("/api/calculations/", json={
            "operation": "add",
            "operand1": 5,
            "operand2": 3
        })
        calc_id = create_response.json()["id"]

        response = authenticated_client.put(f"/api/calculations/{calc_id}", json={
            "operation": "multiply",
            "operand1": 5,
            "operand2": 3
        })
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["operation"] == "multiply"
        assert data["result"] == 15

    def test_delete_calculation(self, authenticated_client):
        """Test deleting a calculation"""
        create_response = authenticated_client.post("/api/calculations/", json={
            "operation": "add",
            "operand1": 5,
            "operand2": 3
        })
        calc_id = create_response.json()["id"]

        response = authenticated_client.delete(f"/api/calculations/{calc_id}")
        assert response.status_code == status.HTTP_200_OK

        # Verify deletion
        get_response = authenticated_client.get(f"/api/calculations/{calc_id}")
        assert get_response.status_code == status.HTTP_404_NOT_FOUND


class TestUserEndpoints:
    """Test user profile endpoints"""

    def test_get_current_user(self, authenticated_client, test_user_data):
        """Test getting current user profile"""
        response = authenticated_client.get("/api/users/me")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["username"] == test_user_data["username"]
        assert data["email"] == test_user_data["email"]

    def test_update_user_profile(self, authenticated_client):
        """Test updating user profile"""
        response = authenticated_client.put("/api/users/me", json={
            "username": "newusername",
            "email": "newemail@example.com"
        })
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["username"] == "newusername"
        assert data["email"] == "newemail@example.com"

    def test_change_password(self, authenticated_client, test_user_data):
        """Test changing password"""
        response = authenticated_client.post("/api/users/me/change-password", json={
            "current_password": test_user_data["password"],
            "new_password": "newpassword123"
        })
        assert response.status_code == status.HTTP_200_OK

    def test_change_password_wrong_current(self, authenticated_client):
        """Test changing password with wrong current password"""
        response = authenticated_client.post("/api/users/me/change-password", json={
            "current_password": "wrongpassword",
            "new_password": "newpassword123"
        })
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_get_user_statistics(self, authenticated_client):
        """Test getting user statistics"""
        # Create some calculations
        authenticated_client.post("/api/calculations/", json={
            "operation": "add",
            "operand1": 5,
            "operand2": 3
        })
        authenticated_client.post("/api/calculations/", json={
            "operation": "add",
            "operand1": 10,
            "operand2": 20
        })
        authenticated_client.post("/api/calculations/", json={
            "operation": "multiply",
            "operand1": 4,
            "operand2": 5
        })

        response = authenticated_client.get("/api/users/me/statistics")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["total_calculations"] == 3
        assert "calculations_by_operation" in data
        assert data["calculations_by_operation"]["add"] == 2
        assert data["calculations_by_operation"]["multiply"] == 1
        assert data["most_used_operation"] == "add"
