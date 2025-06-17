@echo off
chcp 65001
setlocal enabledelayedexpansion

:: 检查虚拟环境
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

:: 检查 C++ 编译器
cl -help >nul 2>nul
if errorlevel 1 (
    echo Installing Microsoft C++ Build Tools...
    powershell -Command "Start-Process 'https://aka.ms/vs/17/release/vs_BuildTools.exe' -ArgumentList '/quiet', '/norestart', '--add', 'Microsoft.VisualStudio.Workload.VCTools' -Wait"
    echo 请手动完成 C++ Build Tools 安装后，重新运行本脚本。
    pause
    exit /b
)

:: 激活虚拟环境
call venv\Scripts\activate.bat

:: 初始化项目环境（依赖安装、目录、.env等）
echo Initializing project...
python init.py setup

:: 启动应用
echo Starting application...
start http://localhost:5000
python main.py

call venv\Scripts\deactivate.bat
endlocal