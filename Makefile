# EmotionSpeak 项目 Makefile

.PHONY: help install format lint test test-cov clean run setup dev

help:  ## 显示帮助信息
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install:  ## 安装项目依赖
	pip install -r requirements.txt

dev-install:  ## 安装开发环境依赖
	pip install -r requirements.txt
	pip install -e .

format:  ## 格式化代码
	black src/ tests/ scripts/ main.py
	@echo "代码格式化完成"

lint:  ## 代码风格检查
	flake8 src/ tests/ scripts/ main.py
	@echo "代码风格检查完成"

test:  ## 运行测试
	pytest -v

test-cov:  ## 运行测试并生成覆盖率报告
	pytest --cov=src --cov-report=html --cov-report=term-missing
	@echo "测试覆盖率报告已生成到 htmlcov/ 目录"

clean:  ## 清理缓存和构建文件
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	@echo "清理完成"

run:  ## 运行主程序
	python main.py

demo:  ## 运行演示程序
	python scripts/demo.py

setup:  ## 项目初始化设置
	python scripts/setup.py

check:  ## 运行所有检查 (格式化 + 代码风格 + 测试)
	$(MAKE) format
	$(MAKE) lint
	$(MAKE) test

build:  ## 构建项目
	python -m build
