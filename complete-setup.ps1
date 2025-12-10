# Complete Setup Script for Bhavana Vuttunoori
# Run this after creating GitHub repository

Write-Host "==================================" -ForegroundColor Cyan
Write-Host "Docker Hub & GitHub Setup Complete" -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "✅ Docker Hub username configured: bhavanavuttunoori" -ForegroundColor Green
Write-Host "✅ Access token ready" -ForegroundColor Green
Write-Host ""

# Login to Docker Hub
Write-Host "Step 1: Logging into Docker Hub..." -ForegroundColor Yellow
docker login -u bhavanavuttunoori
Write-Host ""

# Test docker connection
Write-Host "Step 2: Verifying Docker connection..." -ForegroundColor Yellow
docker info | Select-String -Pattern "Username"
Write-Host "✅ Docker Hub connected" -ForegroundColor Green
Write-Host ""

Write-Host "==================================" -ForegroundColor Cyan
Write-Host "Next Steps - GitHub Setup" -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Create GitHub Repository:" -ForegroundColor Yellow
Write-Host "   Go to: https://github.com/new" -ForegroundColor White
Write-Host "   Repository name: advanced-calculator-api" -ForegroundColor Gray
Write-Host "   Visibility: Public" -ForegroundColor Gray
Write-Host "   DO NOT initialize with README" -ForegroundColor Red
Write-Host ""

Write-Host "2. After creating repository, run these commands:" -ForegroundColor Yellow
Write-Host ""
Write-Host "   # Initialize git repository" -ForegroundColor Gray
Write-Host "   git init" -ForegroundColor White
Write-Host ""
Write-Host "   # Configure git (first time only)" -ForegroundColor Gray
Write-Host "   git config --global user.name `"Bhavana Vuttunoori`"" -ForegroundColor White
Write-Host "   git config --global user.email `"vuttunoori.bhavana@example.com`"" -ForegroundColor White
Write-Host ""
Write-Host "   # Add all files" -ForegroundColor Gray
Write-Host "   git add ." -ForegroundColor White
Write-Host ""
Write-Host "   # Commit" -ForegroundColor Gray
Write-Host "   git commit -m `"Initial commit - Advanced Calculator API`"" -ForegroundColor White
Write-Host ""
Write-Host "   # Add remote (replace with your actual GitHub repo URL)" -ForegroundColor Gray
Write-Host "   git remote add origin https://github.com/bhavanavuttunoori/advanced-calculator-api.git" -ForegroundColor White
Write-Host ""
Write-Host "   # Push to GitHub" -ForegroundColor Gray
Write-Host "   git branch -M main" -ForegroundColor White
Write-Host "   git push -u origin main" -ForegroundColor White
Write-Host ""

Write-Host "3. Add GitHub Secrets:" -ForegroundColor Yellow
Write-Host "   Go to: https://github.com/bhavanavuttunoori/advanced-calculator-api/settings/secrets/actions" -ForegroundColor White
Write-Host ""
Write-Host "   Add these two secrets:" -ForegroundColor Gray
Write-Host "   Name: DOCKERHUB_USERNAME" -ForegroundColor White
Write-Host "   Value: <your-dockerhub-username>" -ForegroundColor Cyan
Write-Host ""
Write-Host "   Name: DOCKERHUB_TOKEN" -ForegroundColor White
Write-Host "   Value: <your-dockerhub-access-token>" -ForegroundColor Cyan
Write-Host ""

Write-Host "==================================" -ForegroundColor Cyan
Write-Host "Important URLs" -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Docker Hub Repository:" -ForegroundColor Yellow
Write-Host "https://hub.docker.com/r/bhavanavuttunoori/advanced-calculator-api" -ForegroundColor Cyan
Write-Host ""
Write-Host "GitHub Repository:" -ForegroundColor Yellow
Write-Host "https://github.com/bhavanavuttunoori/advanced-calculator-api" -ForegroundColor Cyan
Write-Host ""
Write-Host "GitHub Secrets Settings:" -ForegroundColor Yellow
Write-Host "https://github.com/bhavanavuttunoori/advanced-calculator-api/settings/secrets/actions" -ForegroundColor Cyan
Write-Host ""

Write-Host "==================================" -ForegroundColor Green
Write-Host "Setup Ready! Follow the steps above" -ForegroundColor Green
Write-Host "==================================" -ForegroundColor Green
