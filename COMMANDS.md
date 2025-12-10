# Useful Commands Cheat Sheet

## Docker Commands

### Starting and Stopping
```bash
# Start all services
docker-compose up

# Start in background
docker-compose up -d

# Build and start
docker-compose up --build

# Stop all services
docker-compose down

# Stop and remove volumes (reset database)
docker-compose down -v

# View logs
docker-compose logs -f

# View logs for specific service
docker-compose logs -f web
docker-compose logs -f db
```

### Docker Service Management
```bash
# Execute command in running container
docker-compose exec web pytest -v

# Access shell in container
docker-compose exec web bash
docker-compose exec db psql -U fastapi_user -d fastapi_db

# Restart specific service
docker-compose restart web

# View running containers
docker-compose ps

# View resource usage
docker stats
```

## Python/FastAPI Commands

### Running the Application Locally
```bash
# Activate virtual environment
.\venv\Scripts\Activate.ps1   # Windows PowerShell
source venv/bin/activate        # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Run development server
uvicorn app.main:app --reload

# Run on different port
uvicorn app.main:app --reload --port 8001

# Run with custom host
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Database Commands

### Alembic Migrations
```bash
# Create new migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback last migration
alembic downgrade -1

# View migration history
alembic history

# View current version
alembic current

# Rollback to specific version
alembic downgrade <revision_id>
```

### Database Access
```bash
# Connect to PostgreSQL (in Docker)
docker-compose exec db psql -U fastapi_user -d fastapi_db

# Common SQL commands
\dt                 # List tables
\d users           # Describe users table
\d calculations    # Describe calculations table
SELECT * FROM users;
SELECT * FROM calculations;
\q                 # Quit
```

## Testing Commands

### Pytest
```bash
# Run all tests
pytest -v

# Run specific test file
pytest tests/test_unit.py -v
pytest tests/test_integration.py -v
pytest tests/test_e2e.py -v

# Run with coverage
pytest --cov=app --cov-report=html --cov-report=term

# Run specific test
pytest tests/test_unit.py::TestCalculationLogic::test_addition -v

# Run tests matching pattern
pytest -k "test_password" -v

# Stop on first failure
pytest -x

# Show print statements
pytest -s

# Run with detailed output
pytest -vv
```

### Playwright (E2E Tests)
```bash
# Install Playwright browsers
playwright install

# Run E2E tests in headed mode
pytest tests/test_e2e.py --headed

# Run with slow motion
pytest tests/test_e2e.py --headed --slowmo 1000

# Generate test code recorder
playwright codegen http://localhost:8000
```

## Git Commands

### Basic Workflow
```bash
# Check status
git status

# Stage changes
git add .
git add filename.py

# Commit changes
git commit -m "Description of changes"

# Push to GitHub
git push origin main

# Pull latest changes
git pull origin main

# View commit history
git log --oneline
```

### Branch Management
```bash
# Create new branch
git checkout -b feature/feature-name

# Switch branches
git checkout main
git checkout feature/feature-name

# List branches
git branch

# Merge branch
git checkout main
git merge feature/feature-name

# Delete branch
git branch -d feature/feature-name
```

### Undoing Changes
```bash
# Discard changes in working directory
git checkout -- filename.py

# Unstage file
git reset HEAD filename.py

# Amend last commit
git commit --amend -m "New message"

# Reset to last commit (dangerous!)
git reset --hard HEAD
```

## Docker Hub Commands

### Authentication
```bash
# Login to Docker Hub
docker login

# Logout
docker logout
```

### Building and Pushing
```bash
# Build image
docker build -t username/advanced-calculator-api:latest .

# Tag image
docker tag local-image:tag username/advanced-calculator-api:tag

# Push to Docker Hub
docker push username/advanced-calculator-api:latest

# Pull from Docker Hub
docker pull username/advanced-calculator-api:latest

# List local images
docker images

# Remove image
docker rmi username/advanced-calculator-api:latest
```

## Development Tools

### Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate
.\venv\Scripts\Activate.ps1     # Windows PowerShell
.\venv\Scripts\activate.bat     # Windows CMD
source venv/bin/activate         # Linux/Mac

# Deactivate
deactivate

# Install package
pip install package-name

# Update requirements.txt
pip freeze > requirements.txt

# Install from requirements
pip install -r requirements.txt
```

### Code Quality
```bash
# Format code with black
black app/ tests/

# Check with flake8
flake8 app/ tests/

# Type checking with mypy
mypy app/

# Security check
bandit -r app/
```

## Debugging

### Application Debugging
```bash
# Run with Python debugger
python -m pdb app/main.py

# Common pdb commands:
# n - next line
# c - continue
# l - list code
# p variable - print variable
# q - quit

# View application logs
docker-compose logs -f web
```

### Database Debugging
```bash
# Check database connection
docker-compose exec db pg_isready

# View database tables
docker-compose exec db psql -U fastapi_user -d fastapi_db -c "\dt"

# Count records
docker-compose exec db psql -U fastapi_user -d fastapi_db -c "SELECT COUNT(*) FROM users;"

# View recent calculations
docker-compose exec db psql -U fastapi_user -d fastapi_db -c "SELECT * FROM calculations ORDER BY created_at DESC LIMIT 5;"
```

## Performance

### Monitoring
```bash
# View container stats
docker stats

# View disk usage
docker system df

# View container resource usage
docker-compose top
```

### Cleanup
```bash
# Remove unused images
docker image prune -a

# Remove unused volumes
docker volume prune

# Remove unused containers
docker container prune

# Remove everything unused
docker system prune -a --volumes

# Clear pytest cache
rm -rf .pytest_cache
rm -rf __pycache__
```

## API Testing

### Using curl
```bash
# Register user
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","email":"test@example.com","password":"password123"}'

# Login
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"password123"}'

# Create calculation (with token)
curl -X POST http://localhost:8000/api/calculations/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{"operation":"add","operand1":5,"operand2":3}'

# Get calculations
curl -X GET http://localhost:8000/api/calculations/ \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### Using HTTPie (if installed)
```bash
# Install HTTPie
pip install httpie

# Register
http POST :8000/api/auth/register username=testuser email=test@example.com password=password123

# Login
http POST :8000/api/auth/login username=testuser password=password123

# Create calculation
http POST :8000/api/calculations/ Authorization:"Bearer TOKEN" operation=add operand1:=5 operand2:=3
```

## Quick Fixes

### Port Already in Use
```bash
# Windows - Find process on port 8000
netstat -ano | findstr :8000

# Kill process (replace PID)
taskkill /PID <PID> /F

# Linux/Mac - Find process
lsof -i :8000

# Kill process
kill -9 <PID>
```

### Database Connection Issues
```bash
# Reset database
docker-compose down -v
docker-compose up --build

# Check database status
docker-compose exec db pg_isready

# Restart database only
docker-compose restart db
```

### Permission Issues
```bash
# Windows - Run as administrator
# Right-click PowerShell → Run as Administrator

# Linux - Add user to docker group
sudo usermod -aG docker $USER

# Fix file permissions
chmod +x script.sh
```

## Useful Keyboard Shortcuts

### VS Code
- `Ctrl + `` - Toggle terminal
- `Ctrl + P` - Quick file open
- `Ctrl + Shift + F` - Search in files
- `F5` - Start debugging
- `Ctrl + /` - Toggle comment

### Terminal
- `Ctrl + C` - Stop process
- `Ctrl + D` - Exit shell
- `Ctrl + L` - Clear screen
- `Ctrl + R` - Search command history

---

Save this file for quick reference! 🚀
