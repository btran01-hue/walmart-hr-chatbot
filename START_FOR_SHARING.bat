@echo off
echo ========================================
echo LAX2 HR Chatbot - Network Mode
echo ========================================
echo.
echo Starting backend for network access...
echo.
echo Your coworkers will be able to connect to the chatbot!
echo.
echo IMPORTANT: Keep this window open while sharing.
echo Press Ctrl+C to stop the server.
echo.
echo ========================================
echo.

cd backend
call .venv\Scripts\activate

echo Getting your IP address...
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /c:"IPv4 Address"') do (
    set IP=%%a
    goto :found
)
:found
echo.
echo YOUR IP ADDRESS: %IP%
echo.
echo Tell your team to update chatbot.html line 264 to:
echo const API_URL = 'http://%IP%:8000/api/chat';
echo.
echo ========================================
echo Starting server...
echo ========================================
echo.

uvicorn main:app --host 0.0.0.0 --port 8000

pause
