 @echo off
chcp 65001

if "%1"=="" goto usage
if "%1"=="create" goto create
if "%1"=="activate" goto activate
if "%1"=="install" goto install
goto usage

:create
echo 创建虚拟环境...
python -m venv .venv
echo 虚拟环境创建完成！
goto end

:activate
echo 激活虚拟环境...
call .venv\Scripts\activate.bat
goto end

:install
echo 安装依赖...
call .venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt
echo 依赖安装完成！
goto end

:usage
echo 使用方法：
echo venv.bat create    - 创建虚拟环境
echo venv.bat activate  - 激活虚拟环境
echo venv.bat install   - 安装依赖
goto end

:end