@echo off
chcp 65001

echo 启动 EmotionSpeak...

:: 检查虚拟环境是否存在
if not exist ".venv" (
    echo 虚拟环境不存在，正在创建...
    call venv.bat create
    call venv.bat install
)

:: 激活虚拟环境并启动应用
call .venv\Scripts\activate.bat
python main.py

pause