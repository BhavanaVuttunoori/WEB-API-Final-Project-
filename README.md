# Advanced Calculator API - FastAPI Web Application

A full-featured web application built with FastAPI that provides calculator functionality with user authentication, calculation history, and comprehensive statistics. This project demonstrates modern web development practices including REST API design, database management, security implementation, and DevOps workflows.

## Features

### Core Functionality (BREAD Operations)
- Browse: View all calculations for authenticated users
- Read: Retrieve specific calculation details
- Edit: Update existing calculations
- Add: Create new calculations
- Delete: Remove calculations from history

### Advanced Features

#### 1. User Authentication & Authorization
- Secure user registration with email validation
- JWT-based authentication
- Password hashing using bcrypt
- Protected API endpoints

#### 2. Calculator Operations
- Addition
- Subtraction
- Multiplication
- Division with zero-division protection
- Power/Exponentiation
- Modulo

#### 3. User Profile Management
- View and update profile information (username, email)
- Secure password change functionality
- Account deletion with cascade data removal

#### 4. Calculation History & Statistics
- Complete calculation history with timestamps
- Total calculations count
- Average calculation results
- Most frequently used operation
- Operations breakdown by type
- Recent calculations display

### Technology Stack

**Backend:**
- FastAPI - Modern, fast web framework
- SQLAlchemy - SQL toolkit and ORM
- PostgreSQL - Relational database
- Alembic - Database migrations
- Pydantic - Data validation

**Security:**
- JWT tokens for authentication
- Bcrypt password hashing
- OAuth2 with Password flow
- CORS middleware

**Frontend:**
- HTML5, CSS3, JavaScript (Vanilla)
- Responsive design
- Interactive single-page application

**DevOps:**
- Docker & Docker Compose
- GitHub Actions CI/CD
- Automated testing pipeline
- Docker Hub integration

**Testing:**
- Pytest - Testing framework
- Playwright - E2E testing
- Coverage reporting

## Prerequisites

- Python 3.11+
- Docker and Docker Compose
- Git
- PostgreSQL (for local development without Docker)

## Getting Started

### Option 1: Docker Compose (Recommended)

1. Clone the repository
```bash
git clone https://github.com/BhavanaVuttunoori/WEB-API-Final-Project-.git
cd "web api final"
```

2. Start the application
```bash
docker-compose up --build
```

3. Access the application
- Web Interface: http://localhost:8000
- API Documentation: http://localhost:8000/docs
- Alternative API Docs: http://localhost:8000/redoc

### Option 2: Local Development

1. Clone the repository
```bash
git clone https://github.com/BhavanaVuttunoori/WEB-API-Final-Project-.git
cd "web api final"
```

2. Create and activate virtual environment
```bash
python -m venv venv
# On Windows
.\venv\Scripts\activate
# On Linux/Mac
source venv/bin/activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Set up PostgreSQL database
```bash
# Install PostgreSQL and create database
createdb fastapi_db
createuser fastapi_user
```

5. Configure environment variables
```bash
cp .env.example .env
# Edit .env with your database credentials
```

6. Run database migrations
```bash
alembic upgrade head
```

7. Start the development server
```bash
uvicorn app.main:app --reload
```

## Running Tests

### Run All Tests
```bash
pytest -v
```

### Run Specific Test Categories
```bash
# Unit tests only
pytest tests/test_unit.py -v

# Integration tests only
pytest tests/test_integration.py -v

# E2E tests only (requires running application)
pytest tests/test_e2e.py -v
```

### Run with Coverage
```bash
pytest --cov=app --cov-report=html --cov-report=term
```

### E2E Tests with Playwright
```bash
# Install Playwright browsers (first time only)
playwright install

# Run E2E tests
pytest tests/test_e2e.py --headed
```

## Test Coverage

The project includes comprehensive testing:
- Unit Tests: Business logic, calculations, password hashing
- Integration Tests: API endpoints, database interactions, authentication flows
- E2E Tests: Complete user workflows from registration to calculations to profile management

## Database Migrations

### Create a New Migration
```bash
alembic revision --autogenerate -m "Description of changes"
```

### Apply Migrations
```bash
alembic upgrade head
```

### Rollback Migration
```bash
alembic downgrade -1
```

## Docker Hub Deployment

**Docker Hub Repository:** https://hub.docker.com/r/bhavanavuttunoori/advanced-calculator-api

### Manual Docker Build and Push
```bash
# Build the image
docker build -t bhavanavuttunoori/advanced-calculator-api:latest .

# Push to Docker Hub
docker push bhavanavuttunoori/advanced-calculator-api:latest
```

### Pull and Run from Docker Hub
```bash
docker pull bhavanavuttunoori/advanced-calculator-api:latest
docker run -p 8000:8000 \
  -e DATABASE_URL="postgresql://user:pass@host:5432/db" \
  -e SECRET_KEY="your-secret-key" \
  bhavanavuttunoori/advanced-calculator-api:latest
```

## CI/CD Pipeline

The project uses GitHub Actions for continuous integration and deployment:

### Workflow Steps:
1. Test Stage
   - Run unit tests
   - Run integration tests
   - Run E2E tests
   - Generate coverage reports

2. Build Stage (on main branch)
   - Build Docker image
   - Push to Docker Hub
   - Tag with latest and commit SHA

3. Security Scan (optional)
   - Scan Docker image for vulnerabilities
   - Upload results to GitHub Security

### Setup GitHub Actions:

1. Add secrets to your GitHub repository:
   - DOCKERHUB_USERNAME: Your Docker Hub username
   - DOCKERHUB_TOKEN: Your Docker Hub access token

2. Push to main branch to trigger the pipeline

## Project Structure

```
web api final/
├── .github/
│   └── workflows/
│       └── ci-cd.yml          # GitHub Actions workflow
├── alembic/                   # Database migrations
│   ├── versions/              # Migration scripts
│   ├── env.py                 # Alembic environment
│   └── script.py.mako         # Migration template
├── app/
│   ├── routers/               # API route handlers
│   │   ├── auth.py            # Authentication endpoints
│   │   ├── calculations.py    # Calculator BREAD operations
│   │   └── users.py           # User profile management
│   ├── static/                # Frontend files
│   │   ├── index.html         # Main HTML page
│   │   ├── styles.css         # Styling
│   │   └── app.js             # Frontend JavaScript
│   ├── __init__.py
│   ├── auth.py                # Authentication logic
│   ├── config.py              # Configuration management
│   ├── database.py            # Database connection
│   ├── main.py                # FastAPI application
│   ├── models.py              # SQLAlchemy models
│   └── schemas.py             # Pydantic schemas
├── tests/
│   ├── conftest.py            # Test configuration
│   ├── test_unit.py           # Unit tests
│   ├── test_integration.py    # Integration tests
│   └── test_e2e.py            # End-to-end tests
├── .env                       # Environment variables (not in git)
├── .env.example               # Environment template
├── .gitignore                 # Git ignore rules
├── alembic.ini                # Alembic configuration
├── docker-compose.yml         # Docker Compose setup
├── Dockerfile                 # Docker image definition
├── pytest.ini                 # Pytest configuration
├── README.md                  # This file
└── requirements.txt           # Python dependencies
```

## Security Features

- Password Hashing: Bcrypt with automatic salt generation
- JWT Tokens: Secure token-based authentication with expiration
- Input Validation: Pydantic schemas validate all input data
- SQL Injection Protection: SQLAlchemy ORM prevents SQL injection
- CORS: Configurable CORS middleware
- Environment Variables: Sensitive data stored in environment variables

## API Endpoints

### Authentication
- POST /api/auth/register - Register new user
- POST /api/auth/login - Login and get JWT token

### Calculations (Protected)
- GET /api/calculations/ - List all calculations
- POST /api/calculations/ - Create new calculation
- GET /api/calculations/{id} - Get specific calculation
- PUT /api/calculations/{id} - Update calculation
- DELETE /api/calculations/{id} - Delete calculation

### User Profile (Protected)
- GET /api/users/me - Get current user profile
- PUT /api/users/me - Update profile
- POST /api/users/me/change-password - Change password
- GET /api/users/me/statistics - Get calculation statistics
- DELETE /api/users/me - Delete account

## Using the Application

### Registration
1. Navigate to http://localhost:8000
2. Click "Register" link
3. Fill in username, email, and password
4. Click "Register" button

### Login
1. Enter your credentials
2. Click "Login" button

### Calculator
1. Enter first number
2. Select operation
3. Enter second number
4. Click "Calculate"
5. View result

### View History
1. Click "History" in navigation
2. View all past calculations
3. See statistics and breakdowns
4. Delete individual calculations

### Manage Profile
1. Click "Profile" in navigation
2. Update username or email
3. Change password using current and new password
4. Click respective "Update" buttons

## Contributing

1. Fork the repository
2. Create a feature branch (git checkout -b feature/AmazingFeature)
3. Commit your changes (git commit -m 'Add some AmazingFeature')
4. Push to the branch (git push origin feature/AmazingFeature)
5. Open a Pull Request

## License

This project is created for educational purposes as part of a web development course.

## Author

**Bhavana Vuttunoori**
- GitHub: @BhavanaVuttunoori
- GitHub Repository: https://github.com/BhavanaVuttunoori/WEB-API-Final-Project-
- Docker Hub: https://hub.docker.com/u/bhavanavuttunoori

## Acknowledgments

- FastAPI documentation and community
- SQLAlchemy documentation
- Playwright testing framework
- Course instructors and peers

## Support

For support, please open an issue in the GitHub repository or contact the project maintainer.

---

## Project Requirements Checklist

### Functionality 
- All BREAD operations working
- User profile & password change feature
- Calculation history and statistics

### Code Quality & Organization 
- Clean, well-organized code
- Follows best practices
- Comprehensive comments

### Security 
- JWT authentication
- Bcrypt password hashing
- Input validation with Pydantic
- Secure password storage

### Testing 
- Comprehensive unit tests
- Integration tests
- E2E tests with Playwright
- All tests passing

### CI/CD Pipeline 
- GitHub Actions configured
- Automated testing
- Docker build and push
- Deployment to Docker Hub

### Documentation
- Thorough README
- Setup instructions
- Testing instructions
- API documentation

### Front-End Integration
- Seamless integration with backend
- Smooth and intuitive UX
- Responsive design

### Innovation & Extra Features 
- Additional operations (power, modulo)
- Comprehensive statistics
- Password change feature
- Profile management

