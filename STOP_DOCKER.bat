@echo off
REM ============================================
REM Walmart HR Chatbot - Docker Stop Script
REM ============================================

echo.
echo Stopping HR Chatbot...
echo.

docker-compose down

echo.
echo Chatbot stopped!
echo.
echo To restart, run START_DOCKER.bat
echo.
pause
