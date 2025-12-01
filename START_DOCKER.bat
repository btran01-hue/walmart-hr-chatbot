@echo off
REM ============================================
REM Walmart HR Chatbot - Docker Startup Script
REM ============================================

echo.
echo  _    _ ____     _____ _           _   _           _   
echo | |  | |  _ \   / ____| |         | | | |         | |  
echo | |__| | |_) | | |    | |__   __ _| |_| |__   ___ | |_ 
echo |  __  |  _ ^<  | |    | '_ \ / _` | __| '_ \ / _ \| __|
echo | |  | | |_) | | |____| | | | (_| | |_| |_) | (_) | |_ 
echo |_|  |_|____/   \_____|_| |_|\__,_|\__|_.__/ \___/ \__|
echo.
echo ============================================
echo Starting HR Chatbot with Docker...
echo ============================================
echo.

REM Check if Docker is running
docker info >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Docker is not running!
    echo Please start Docker Desktop first.
    echo.
    pause
    exit /b 1
)

REM Check if .env exists
if not exist .env (
    echo [WARNING] No .env file found!
    echo Creating from .env.example...
    copy .env.example .env
    echo.
    echo Please edit .env and add your OPENAI_API_KEY
    echo Then run this script again.
    echo.
    notepad .env
    pause
    exit /b 1
)

echo [1/3] Building containers...
docker-compose build

if errorlevel 1 (
    echo [ERROR] Build failed!
    pause
    exit /b 1
)

echo.
echo [2/3] Starting containers...
docker-compose up -d

if errorlevel 1 (
    echo [ERROR] Failed to start containers!
    pause
    exit /b 1
)

echo.
echo [3/3] Waiting for services to be ready...
timeout /t 10 /nobreak >nul

REM Check health
docker-compose ps

echo.
echo ============================================
echo SUCCESS! Chatbot is now running!
echo ============================================
echo.
echo Access the chatbot at:
echo   Local:   http://localhost
echo.

REM Get IP address for sharing
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /c:"IPv4 Address"') do (
    set IP=%%a
    goto :found
)
:found
if defined IP (
    echo   Network: http:%IP%
    echo.
    echo Share the Network URL with your team!
)

echo.
echo Commands:
echo   Stop:    docker-compose down
echo   Logs:    docker-compose logs -f
echo   Restart: docker-compose restart
echo.
pause
