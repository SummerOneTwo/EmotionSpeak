@echo off
chcp 65001 > nul

echo [INFO] Starting EmotionSpeak...

:: Check if virtual environment exists
if not exist ".venv" (
    echo [INFO] Virtual environment not found, creating...
    call venv.bat create
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to create virtual environment
        pause
        exit /b 1
    )
    call venv.bat install
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to install dependencies
        pause
        exit /b 1
    )
)

:: Activate virtual environment and start application
call .venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo [ERROR] Failed to activate virtual environment
    pause
    exit /b 1
)

python main.py
if %errorlevel% neq 0 (
    echo [ERROR] Application failed to start
    pause
    exit /b 1
)

pause