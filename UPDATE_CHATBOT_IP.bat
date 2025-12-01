@echo off
color 0A
echo ========================================
echo   LAX2 HR Chatbot - IP Updater
echo ========================================
echo.
echo This script will automatically update
echo chatbot.html with your IP address!
echo.
echo ========================================
echo.

:: Get the IP address automatically
echo Detecting your IP address...
echo.

for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /c:"IPv4 Address"') do (
    set RAW_IP=%%a
    goto :found
)

:found
:: Trim spaces from IP
for /f "tokens=* delims= " %%a in ("%RAW_IP%") do set IP=%%a

echo Found your IP address: %IP%
echo.
echo ========================================
echo.
echo I will update chatbot.html to use:
echo http://%IP%:8000/api/chat
echo.
echo Is this correct?
echo.
set /p CONFIRM="Type YES to continue or NO to enter manually: "

if /i "%CONFIRM%"=="YES" goto :update
if /i "%CONFIRM%"=="Y" goto :update

echo.
set /p IP="Enter your IP address (e.g., 192.168.1.100): "

:update
echo.
echo ========================================
echo Updating chatbot.html...
echo ========================================
echo.

:: Backup the original file first
if not exist "chatbot.html.backup" (
    copy chatbot.html chatbot.html.backup >nul
    echo Created backup: chatbot.html.backup
)

:: Use PowerShell to update the file (more reliable than batch)
powershell -Command "(Get-Content 'chatbot.html') -replace 'http://localhost:8000', 'http://%IP%:8000' | Set-Content 'chatbot.html'"

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo   SUCCESS! File Updated!
    echo ========================================
    echo.
    echo Your chatbot.html now uses:
    echo http://%IP%:8000/api/chat
    echo.
    echo ========================================
    echo   NEXT STEPS:
    echo ========================================
    echo.
    echo 1. Start the backend by running:
    echo    START_FOR_SHARING.bat
    echo.
    echo 2. Share chatbot.html with your team:
    echo    - Email it to them
    echo    - Copy to shared drive
    echo    - Upload to SharePoint
    echo.
    echo 3. They just open it in their browser!
    echo.
    echo ========================================
    echo.
    echo NOTE: A backup was saved as:
    echo chatbot.html.backup
    echo.
) else (
    echo.
    echo ========================================
    echo   ERROR!
    echo ========================================
    echo.
    echo Something went wrong. Please try:
    echo 1. Run this script as Administrator
    echo 2. Or manually edit chatbot.html
    echo.
)

echo.
pause
