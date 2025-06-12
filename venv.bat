@echo off
chcp 65001 > nul

if "%1"=="" goto usage
if "%1"=="create" goto create
if "%1"=="activate" goto activate
if "%1"=="install" goto install
goto usage

:create
echo [INFO] Creating virtual environment...
python -m venv .venv
echo [INFO] Virtual environment created successfully!
goto end

:activate
echo [INFO] Activating virtual environment...
call .venv\Scripts\activate.bat
goto end

:install
echo [INFO] Installing dependencies...
call .venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt
echo [INFO] Dependencies installed successfully!
goto end

:usage
echo Usage:
echo venv.bat create    - Create virtual environment
echo venv.bat activate  - Activate virtual environment
echo venv.bat install   - Install dependencies
goto end

:end