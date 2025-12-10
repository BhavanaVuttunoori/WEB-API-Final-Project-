"""End-to-End tests using Playwright"""
import pytest
from playwright.sync_api import Page, expect
import time


@pytest.fixture(scope="module")
def base_url():
    """Base URL for the application"""
    return "http://localhost:8000"


class TestAuthenticationFlow:
    """Test complete authentication workflows"""

    def test_registration_and_login(self, page: Page, base_url: str):
        """Test user registration and login flow"""
        page.goto(base_url)
        
        # Click register link
        page.click("#show-register")
        time.sleep(0.5)
        
        # Fill registration form
        timestamp = int(time.time())
        username = f"testuser_{timestamp}"
        email = f"test_{timestamp}@example.com"
        password = "testpassword123"
        
        page.fill("#register-username", username)
        page.fill("#register-email", email)
        page.fill("#register-password", password)
        page.click("#register-form button[type='submit']")
        
        # Wait for success message and redirect
        time.sleep(1)
        
        # Should be on login page now
        expect(page.locator("#login-page")).to_be_visible()
        
        # Login with new credentials
        page.fill("#login-username", username)
        page.fill("#login-password", password)
        page.click("#login-form button[type='submit']")
        
        # Wait for calculator page
        time.sleep(1)
        expect(page.locator("#calculator-page")).to_be_visible()

    def test_login_with_wrong_credentials(self, page: Page, base_url: str):
        """Test login with incorrect credentials"""
        page.goto(base_url)
        
        page.fill("#login-username", "nonexistent")
        page.fill("#login-password", "wrongpassword")
        page.click("#login-form button[type='submit']")
        
        # Should see error message
        time.sleep(1)
        expect(page.locator(".toast.error")).to_be_visible()


class TestCalculatorFlow:
    """Test calculator functionality"""

    @pytest.fixture(autouse=True)
    def setup(self, page: Page, base_url: str):
        """Setup: Login before each test"""
        page.goto(base_url)
        
        # Register a new user
        page.click("#show-register")
        time.sleep(0.5)
        
        timestamp = int(time.time())
        self.username = f"calcuser_{timestamp}"
        self.email = f"calc_{timestamp}@example.com"
        self.password = "testpassword123"
        
        page.fill("#register-username", self.username)
        page.fill("#register-email", self.email)
        page.fill("#register-password", self.password)
        page.click("#register-form button[type='submit']")
        time.sleep(1)
        
        # Login
        page.fill("#login-username", self.username)
        page.fill("#login-password", self.password)
        page.click("#login-form button[type='submit']")
        time.sleep(1)

    def test_addition_calculation(self, page: Page):
        """Test addition calculation"""
        page.fill("#operand1", "15")
        page.select_option("#operation", "add")
        page.fill("#operand2", "25")
        page.click("#calculator-form button[type='submit']")
        
        time.sleep(1)
        result = page.locator("#result")
        expect(result).to_contain_text("40")

    def test_division_calculation(self, page: Page):
        """Test division calculation"""
        page.fill("#operand1", "100")
        page.select_option("#operation", "divide")
        page.fill("#operand2", "5")
        page.click("#calculator-form button[type='submit']")
        
        time.sleep(1)
        result = page.locator("#result")
        expect(result).to_contain_text("20")

    def test_power_calculation(self, page: Page):
        """Test power calculation"""
        page.fill("#operand1", "2")
        page.select_option("#operation", "power")
        page.fill("#operand2", "8")
        page.click("#calculator-form button[type='submit']")
        
        time.sleep(1)
        result = page.locator("#result")
        expect(result).to_contain_text("256")

    def test_division_by_zero(self, page: Page):
        """Test division by zero error"""
        page.fill("#operand1", "10")
        page.select_option("#operation", "divide")
        page.fill("#operand2", "0")
        page.click("#calculator-form button[type='submit']")
        
        time.sleep(1)
        expect(page.locator(".toast.error")).to_be_visible()


class TestHistoryFlow:
    """Test history and statistics functionality"""

    @pytest.fixture(autouse=True)
    def setup(self, page: Page, base_url: str):
        """Setup: Login and create calculations"""
        page.goto(base_url)
        
        # Register and login
        page.click("#show-register")
        time.sleep(0.5)
        
        timestamp = int(time.time())
        self.username = f"histuser_{timestamp}"
        self.email = f"hist_{timestamp}@example.com"
        self.password = "testpassword123"
        
        page.fill("#register-username", self.username)
        page.fill("#register-email", self.email)
        page.fill("#register-password", self.password)
        page.click("#register-form button[type='submit']")
        time.sleep(1)
        
        page.fill("#login-username", self.username)
        page.fill("#login-password", self.password)
        page.click("#login-form button[type='submit']")
        time.sleep(1)
        
        # Create some calculations
        calculations = [
            ("5", "add", "3"),
            ("10", "multiply", "2"),
            ("100", "divide", "4"),
        ]
        
        for op1, operation, op2 in calculations:
            page.fill("#operand1", op1)
            page.select_option("#operation", operation)
            page.fill("#operand2", op2)
            page.click("#calculator-form button[type='submit']")
            time.sleep(0.5)

    def test_view_history(self, page: Page):
        """Test viewing calculation history"""
        page.click("#nav-history")
        time.sleep(1)
        
        expect(page.locator("#history-page")).to_be_visible()
        
        # Check that calculations are displayed
        rows = page.locator("#history-tbody tr")
        expect(rows).to_have_count(3)

    def test_view_statistics(self, page: Page):
        """Test viewing statistics"""
        page.click("#nav-history")
        time.sleep(1)
        
        # Check statistics are displayed
        expect(page.locator("#stat-total")).to_contain_text("3")
        expect(page.locator(".operations-breakdown")).to_be_visible()

    def test_delete_calculation(self, page: Page):
        """Test deleting a calculation from history"""
        page.click("#nav-history")
        time.sleep(1)
        
        # Click first delete button
        initial_count = page.locator("#history-tbody tr").count()
        page.click("#history-tbody tr:first-child button.btn-danger")
        
        # Confirm deletion (if there's a confirm dialog)
        page.on("dialog", lambda dialog: dialog.accept())
        
        time.sleep(1)
        
        # Check that row count decreased
        new_count = page.locator("#history-tbody tr").count()
        assert new_count < initial_count


class TestProfileFlow:
    """Test profile management functionality"""

    @pytest.fixture(autouse=True)
    def setup(self, page: Page, base_url: str):
        """Setup: Login before each test"""
        page.goto(base_url)
        
        # Register and login
        page.click("#show-register")
        time.sleep(0.5)
        
        timestamp = int(time.time())
        self.username = f"profuser_{timestamp}"
        self.email = f"prof_{timestamp}@example.com"
        self.password = "testpassword123"
        
        page.fill("#register-username", self.username)
        page.fill("#register-email", self.email)
        page.fill("#register-password", self.password)
        page.click("#register-form button[type='submit']")
        time.sleep(1)
        
        page.fill("#login-username", self.username)
        page.fill("#login-password", self.password)
        page.click("#login-form button[type='submit']")
        time.sleep(1)

    def test_view_profile(self, page: Page):
        """Test viewing profile"""
        page.click("#nav-profile")
        time.sleep(1)
        
        expect(page.locator("#profile-page")).to_be_visible()
        expect(page.locator("#profile-username")).to_have_value(self.username)
        expect(page.locator("#profile-email")).to_have_value(self.email)

    def test_update_profile(self, page: Page):
        """Test updating profile information"""
        page.click("#nav-profile")
        time.sleep(1)
        
        # Update username
        new_username = f"updated_{self.username}"
        page.fill("#profile-username", new_username)
        page.click("#profile-form button[type='submit']")
        
        time.sleep(1)
        expect(page.locator(".toast.success")).to_be_visible()

    def test_change_password(self, page: Page):
        """Test changing password"""
        page.click("#nav-profile")
        time.sleep(1)
        
        # Change password
        page.fill("#current-password", self.password)
        page.fill("#new-password", "newpassword456")
        page.click("#password-form button[type='submit']")
        
        time.sleep(1)
        expect(page.locator(".toast.success")).to_be_visible()
        
        # Verify password field is cleared
        expect(page.locator("#current-password")).to_have_value("")
        expect(page.locator("#new-password")).to_have_value("")

    def test_logout(self, page: Page):
        """Test logout functionality"""
        page.click("#logout-btn")
        time.sleep(1)
        
        # Should be back on login page
        expect(page.locator("#login-page")).to_be_visible()
