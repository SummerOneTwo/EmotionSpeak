# EmotionSpeak 项目 Makefile

VENV_DIR=.venv
PYTHON=$(VENV_DIR)/Scripts/python.exe
PIP=$(VENV_DIR)/Scripts/pip.exe

.PHONY: help install format lint test test-cov clean run setup dev

venv-check:
	@if not exist $(VENV_DIR) (
		echo 未检测到虚拟环境，正在自动创建...
		python -m venv $(VENV_DIR)
	)

help:  ## 显示帮助信息
	@findstr /R /C:"^[a-zA-Z_-]*:.*##" Makefile | sort

install: venv-check  ## 安装项目依赖
	$(PIP) install -r requirements.txt

dev-install: venv-check  ## 安装开发环境依赖
	$(PIP) install -r requirements.txt
	$(PIP) install -e .

format: venv-check  ## 格式化代码
	$(PYTHON) -m black src/ tests/ scripts/ main.py
	@echo 代码格式化完成

lint: venv-check  ## 代码风格检查
	$(PYTHON) -m flake8 src/ tests/ scripts/ main.py
	@echo 代码风格检查完成

test: venv-check  ## 运行测试
	$(PYTHON) -m pytest -v

test-cov: venv-check  ## 运行测试并生成覆盖率报告
	$(PYTHON) -m pytest --cov=src --cov-report=html --cov-report=term-missing
	@echo 测试覆盖率报告已生成到 htmlcov/ 目录

clean:  ## 清理缓存和构建文件
	for /r %%i in (*.pyc) do del /f /q "%%i"
	for /d /r %%i in (__pycache__) do rmdir /s /q "%%i"
	rmdir /s /q .pytest_cache 2>nul
	rmdir /s /q htmlcov 2>nul
	del /f /q .coverage 2>nul
	rmdir /s /q build 2>nul
	rmdir /s /q dist 2>nul
	rmdir /s /q *.egg-info 2>nul
	@echo 清理完成

run: venv-check  ## 运行主程序
	$(PYTHON) main.py

demo: venv-check  ## 运行演示程序
	$(PYTHON) scripts/demo.py

setup: venv-check  ## 项目初始化设置
	$(PYTHON) scripts/setup.py

check:  ## 运行所有检查 (格式化 + 代码风格 + 测试)
	$(MAKE) format
	$(MAKE) lint
	$(MAKE) test

build: venv-check  ## 构建项目
	$(PYTHON) -m build
