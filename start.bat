@echo off
setlocal enabledelayedexpansion

:: 检查虚拟环境
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
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