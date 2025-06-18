@echo off
chcp 65001
setlocal enabledelayedexpansion

echo [1/6] 开始执行脚本...

echo 检查虚拟环境...
if not exist "venv" (
    echo [2/6] 创建虚拟环境...
    python -m venv venv
) else (
    echo [2/6] 虚拟环境已存在
)

echo 检查 C++ 编译器...
cl >nul 2>nul
if %errorlevel% equ 0 (
    echo [3/6] C++ 编译器检查通过
) else (
    echo [3/6] 未找到 C++ 编译器，开始安装...
    echo 正在下载安装程序...
    powershell -Command "Start-Process 'https://aka.ms/vs/17/release/vs_BuildTools.exe' -ArgumentList '/quiet', '/norestart', '--add', 'Microsoft.VisualStudio.Workload.VCTools' -Wait"
    echo 请手动完成 C++ Build Tools 安装后，重新运行本脚本。
    pause
    exit /b 1
)

echo 激活虚拟环境...
call venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo 虚拟环境激活失败！
    pause
    exit /b 1
)

echo 初始化项目环境...
python init.py all
if %errorlevel% neq 0 (
    echo 项目初始化失败！
    pause
    exit /b 1
)

echo 启动应用...
start "" python main.py
timeout /t 10 >nul
start http://127.0.0.1:5000

call venv\Scripts\deactivate.bat
endlocal