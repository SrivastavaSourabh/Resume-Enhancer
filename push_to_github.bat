@echo off
echo ========================================
echo GitHub Push Helper Script
echo ========================================
echo.

if "%1"=="" (
    echo Usage: push_to_github.bat YOUR_GITHUB_REPO_URL
    echo.
    echo Example: push_to_github.bat https://github.com/username/repo-name.git
    echo.
    echo Please provide your GitHub repository URL.
    pause
    exit /b 1
)

set REPO_URL=%1

echo Adding remote repository...
git remote add origin %REPO_URL% 2>nul
if errorlevel 1 (
    echo Remote might already exist. Updating...
    git remote set-url origin %REPO_URL%
)

echo.
echo Setting branch to main...
git branch -M main

echo.
echo Pushing to GitHub...
git push -u origin main

if errorlevel 1 (
    echo.
    echo ========================================
    echo Push failed. Possible reasons:
    echo 1. Authentication required (use Personal Access Token)
    echo 2. Repository doesn't exist or URL is incorrect
    echo 3. Network issues
    echo.
    echo If authentication is needed, GitHub will prompt you.
    echo For HTTPS, use a Personal Access Token as password.
    echo ========================================
) else (
    echo.
    echo ========================================
    echo SUCCESS! Your code has been pushed to GitHub!
    echo ========================================
)

pause

