"""Unit tests for business logic and utility functions"""
import pytest
from app.routers.calculations import perform_calculation
from app.models import OperationType
from app.auth import verify_password, get_password_hash


class TestCalculationLogic:
    """Test calculation logic"""

    def test_addition(self):
        """Test addition operation"""
        result = perform_calculation(OperationType.ADD, 5, 3)
        assert result == 8

    def test_subtraction(self):
        """Test subtraction operation"""
        result = perform_calculation(OperationType.SUBTRACT, 10, 4)
        assert result == 6

    def test_multiplication(self):
        """Test multiplication operation"""
        result = perform_calculation(OperationType.MULTIPLY, 6, 7)
        assert result == 42

    def test_division(self):
        """Test division operation"""
        result = perform_calculation(OperationType.DIVIDE, 15, 3)
        assert result == 5

    def test_division_by_zero(self):
        """Test division by zero raises error"""
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            perform_calculation(OperationType.DIVIDE, 10, 0)

    def test_power(self):
        """Test power operation"""
        result = perform_calculation(OperationType.POWER, 2, 3)
        assert result == 8

    def test_modulo(self):
        """Test modulo operation"""
        result = perform_calculation(OperationType.MODULO, 10, 3)
        assert result == 1

    def test_modulo_by_zero(self):
        """Test modulo by zero raises error"""
        with pytest.raises(ValueError, match="Cannot perform modulo by zero"):
            perform_calculation(OperationType.MODULO, 10, 0)

    def test_negative_numbers(self):
        """Test operations with negative numbers"""
        assert perform_calculation(OperationType.ADD, -5, 3) == -2
        assert perform_calculation(OperationType.MULTIPLY, -4, -3) == 12

    def test_decimal_numbers(self):
        """Test operations with decimal numbers"""
        result = perform_calculation(OperationType.ADD, 1.5, 2.3)
        assert abs(result - 3.8) < 0.0001


class TestPasswordHashing:
    """Test password hashing functionality"""

    def test_password_hash(self):
        """Test that password is hashed correctly"""
        password = "mypassword123"
        hashed = get_password_hash(password)
        assert hashed != password
        assert len(hashed) > 20

    def test_verify_correct_password(self):
        """Test verifying correct password"""
        password = "mypassword123"
        hashed = get_password_hash(password)
        assert verify_password(password, hashed) is True

    def test_verify_incorrect_password(self):
        """Test verifying incorrect password"""
        password = "mypassword123"
        hashed = get_password_hash(password)
        assert verify_password("wrongpassword", hashed) is False

    def test_different_hashes_for_same_password(self):
        """Test that same password produces different hashes (salt)"""
        password = "mypassword123"
        hash1 = get_password_hash(password)
        hash2 = get_password_hash(password)
        assert hash1 != hash2
        assert verify_password(password, hash1)
        assert verify_password(password, hash2)
