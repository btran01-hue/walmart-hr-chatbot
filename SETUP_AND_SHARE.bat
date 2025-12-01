@echo off
color 0B
title LAX2 HR Chatbot - Easy Setup & Share

echo ========================================
echo   LAX2 HR CHATBOT
echo   Easy Setup ^& Share Wizard
echo ========================================
echo.
echo This wizard will:
echo  1. Detect your IP address
echo  2. Update chatbot.html automatically
echo  3. Start the backend server
echo  4. Show you how to share with your team
echo.
echo Press any key to start...
pause >nul
cls

echo ========================================
echo   STEP 1: Finding Your IP Address
echo ========================================
echo.
echo Scanning network...
echo.

:: Get the IP address
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /c:"IPv4 Address"') do (
    set RAW_IP=%%a
    goto :found
)

:found
:: Trim spaces
for /f "tokens=* delims= " %%a in ("%RAW_IP%") do set IP=%%a

echo Found: %IP%
echo.
echo This is the address your team will use to connect!
echo.
pause
cls

echo ========================================
echo   STEP 2: Updating chatbot.html
echo ========================================
echo.
echo Updating chatbot.html to use: %IP%
echo.

:: Backup first
if not exist "chatbot.html.backup" (
    copy chatbot.html chatbot.html.backup >nul
    echo Created backup file
)

:: Update the file
powershell -Command "(Get-Content 'chatbot.html') -replace 'http://localhost:8000', 'http://%IP%:8000' | Set-Content 'chatbot.html'" 2>nul

if %ERRORLEVEL% EQU 0 (
    echo Updated successfully!
) else (
    echo Warning: Could not update automatically
    echo You can do it manually - see instructions below
)

echo.
pause
cls

echo ========================================
echo   STEP 3: Starting Backend Server
echo ========================================
echo.
echo Starting the backend server...
echo This will allow others to connect!
echo.
echo IMPORTANT: Keep this window open!
echo.
echo Your chatbot is accessible at:
echo http://%IP%:8000
echo.
echo ========================================
echo   HOW TO SHARE WITH YOUR TEAM:
echo ========================================
echo.
echo Option 1: EMAIL
echo   - Attach 'chatbot.html' to an email
echo   - Send to your team
echo   - They just open it!
echo.
echo Option 2: SHARED DRIVE
echo   - Copy 'chatbot.html' to network share
echo   - Tell team where to find it
echo.
echo Option 3: SHAREPOINT
echo   - Upload 'chatbot.html' to SharePoint
echo   - Share the link
echo.
echo ========================================
echo.
echo Press any key to start the server...
pause >nul

echo.
echo ========================================
echo   SERVER STARTING...
echo ========================================
echo.
echo Backend URL: http://%IP%:8000
echo Chatbot ready to use!
echo.
echo Press Ctrl+C to stop the server
echo ========================================
echo.

cd backend
call .venv\Scripts\activate
uvicorn main:app --host 0.0.0.0 --port 8000

pause
