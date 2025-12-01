@echo off
echo ========================================
echo   LAX2 HR Chatbot Service
echo ========================================
echo.
echo Starting backend server...
echo.

cd /d C:\Apps\walmart-hr-chatbot\backend

if not exist ".venv" (
    echo ERROR: Virtual environment not found!
    echo Please run setup first.
    echo.
    pause
    exit /b 1
)

call .venv\Scripts\activate

if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Could not activate virtual environment!
    echo.
    pause
    exit /b 1
)

echo ========================================
echo LAX2 HR Chatbot is now running!
echo ========================================
echo.
echo Server is available at:
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /c:"IPv4 Address"') do (
    set RAW_IP=%%a
    goto :found
)
:found
for /f "tokens=* delims= " %%a in ("%RAW_IP%") do set IP=%%a
echo http://%IP%:8000
echo.
echo Health check: http://%IP%:8000/health
echo.
echo ========================================
echo.
echo This window must stay open!
echo DO NOT CLOSE THIS WINDOW!
echo.
echo To stop the server, press Ctrl+C
echo ========================================
echo.
echo [%date% %time%] Starting uvicorn...
echo.

uvicorn main:app --host 0.0.0.0 --port 8000 --log-level info

echo.
echo ========================================
echo Server stopped at: %date% %time%
echo ========================================
echo.
pause
