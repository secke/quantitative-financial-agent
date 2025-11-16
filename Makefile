.PHONY: help install test clean run-example setup venv

# Colors for output
BLUE := \033[0;34m
GREEN := \033[0;32m
YELLOW := \033[0;33m
NC := \033[0m # No Color

help: ## Show this help message
	@echo "$(BLUE)Financial Agent - Available Commands$(NC)"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(GREEN)%-15s$(NC) %s\n", $$1, $$2}'

setup: ## Complete setup (venv + install + config)
	@echo "$(BLUE)Setting up Financial Agent...$(NC)"
	python3 -m venv venv
	@echo "$(GREEN)✓ Virtual environment created$(NC)"
	@echo "$(YELLOW)Run: source venv/bin/activate$(NC)"
	@echo "$(YELLOW)Then run: make install$(NC)"

install: ## Install all dependencies
	@echo "$(BLUE)Installing dependencies...$(NC)"
	pip install --upgrade pip
	pip install -r requirements.txt
	@echo "$(GREEN)✓ Dependencies installed$(NC)"
	@echo "$(YELLOW)Don't forget to configure .env with your HF_TOKEN!$(NC)"

test: ## Run all tests
	@echo "$(BLUE)Running tests...$(NC)"
	python tests/test_tools.py

test-quick: ## Quick test (just market data)
	@echo "$(BLUE)Running quick test...$(NC)"
	python -c "from src.tools.market_data import fetch_stock_data; import json; print(json.dumps(json.loads(fetch_stock_data('AAPL', '5d')), indent=2))"

run-example: ## Run basic usage example
	@echo "$(BLUE)Running basic example...$(NC)"
	python examples/basic_usage.py

notebook: ## Start Jupyter notebook
	@echo "$(BLUE)Starting Jupyter notebook...$(NC)"
	jupyter notebook notebooks/exploration.ipynb

clean: ## Clean cache and logs
	@echo "$(BLUE)Cleaning cache and logs...$(NC)"
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	rm -rf logs/*.log
	@echo "$(GREEN)✓ Cleaned$(NC)"

clean-all: clean ## Clean everything including venv
	@echo "$(BLUE)Removing virtual environment...$(NC)"
	rm -rf venv
	@echo "$(GREEN)✓ Cleaned all$(NC)"

lint: ## Run code linter
	@echo "$(BLUE)Running linter...$(NC)"
	flake8 src/ --max-line-length=120 --exclude=venv

format: ## Format code with black
	@echo "$(BLUE)Formatting code...$(NC)"
	black src/ tests/ examples/

check-env: ## Check if .env is configured
	@echo "$(BLUE)Checking environment configuration...$(NC)"
	@if [ ! -f .env ]; then \
		echo "$(YELLOW)⚠ .env file not found. Copy .env.example to .env$(NC)"; \
	else \
		echo "$(GREEN)✓ .env file exists$(NC)"; \
	fi
	@if grep -q "HF_TOKEN=$$" .env 2>/dev/null; then \
		echo "$(YELLOW)⚠ HF_TOKEN not configured in .env$(NC)"; \
	else \
		echo "$(GREEN)✓ HF_TOKEN configured$(NC)"; \
	fi

dev: ## Install development dependencies
	@echo "$(BLUE)Installing development dependencies...$(NC)"
	pip install black flake8 ipykernel jupyter
	@echo "$(GREEN)✓ Dev dependencies installed$(NC)"

status: ## Show project status
	@echo "$(BLUE)Project Status:$(NC)"
	@echo ""
	@echo "Files created:"
	@find . -type f -name "*.py" | wc -l | xargs echo "  Python files:"
	@find . -type f -name "*.md" | wc -l | xargs echo "  Markdown files:"
	@echo ""
	@echo "Tools implemented:"
	@grep -c "^@tool" src/tools/*.py | sed 's/src\/tools\//  /' | sed 's/.py:/ - /'
	@echo ""
	@if [ -d "venv" ]; then \
		echo "$(GREEN)✓ Virtual environment exists$(NC)"; \
	else \
		echo "$(YELLOW)✗ Virtual environment not created$(NC)"; \
	fi

info: ## Show project information
	@echo "$(BLUE)╔════════════════════════════════════════════╗$(NC)"
	@echo "$(BLUE)║     Financial Agent - Quick Info          ║$(NC)"
	@echo "$(BLUE)╚════════════════════════════════════════════╝$(NC)"
	@echo ""
	@echo "$(GREEN)Location:$(NC) /home/claude/financial-agent"
	@echo "$(GREEN)Tools:$(NC) 6 (Market Data + Technical Analysis)"
	@echo "$(GREEN)Model:$(NC) Llama 3.1 8B via HuggingFace API"
	@echo ""
	@echo "$(YELLOW)Quick Start:$(NC)"
	@echo "  1. make setup"
	@echo "  2. source venv/bin/activate"
	@echo "  3. make install"
	@echo "  4. Edit .env with your HF_TOKEN"
	@echo "  5. make test"
	@echo ""
	@echo "$(YELLOW)For help:$(NC) make help"
