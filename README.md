# Financial Agent

An AI-powered financial analysis agent built with HuggingFace's `smolagents` framework. This agent uses open-source language models to perform comprehensive stock market analysis, technical indicator calculations, and generate trading insights through natural language interactions.

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Web UI](#web-ui)
- [Core Components](#core-components)
- [Usage Examples](#usage-examples)
- [Tools & Capabilities](#tools--capabilities)
- [Configuration](#configuration)
- [Development](#development)
- [Testing](#testing)
- [Limitations](#limitations)
- [Future Enhancements](#future-enhancements)
- [Contributing](#contributing)

## Overview

Financial Agent is an intelligent system that combines the power of large language models (LLMs) with specialized financial analysis tools. It can understand natural language queries about stocks and automatically orchestrate multiple tools to provide comprehensive market analysis.

**Key Capabilities:**
- Real-time stock data retrieval from Yahoo Finance
- Technical analysis with 10+ indicators (RSI, MACD, Moving Averages, Bollinger Bands, etc.)
- Support and resistance level detection
- Volatility and risk analysis
- Automated trading signal generation
- Multi-stock comparison and portfolio monitoring
- Natural language interaction (ask questions in plain English)

**Technology Stack:**
- **AI Framework:** smolagents (HuggingFace's agentic framework)
- **LLM:** Meta Llama 3.1 8B Instruct (via HuggingFace Inference API)
- **Financial Data:** yfinance (Yahoo Finance API)
- **Technical Analysis:** ta-lib (Technical Analysis library)
- **Backend:** Python 3.9+, pandas, numpy

## Architecture

The project follows a modular architecture designed for extensibility and maintainability:

```
financial-agent/
├── src/
│   ├── agents/          # AI Agent implementation
│   │   └── financial_agent.py    # Main agent class with reasoning logic
│   ├── tools/           # Tool implementations (agent capabilities)
│   │   ├── market_data.py        # Market data retrieval tools
│   │   └── technical_analysis.py # Technical indicator tools
│   ├── config/          # Configuration management
│   │   └── settings.py           # Environment variables & settings
│   └── utils/           # Utilities
│       └── logger.py             # Logging system
├── examples/            # Usage examples
├── tests/              # Unit tests
├── notebooks/          # Jupyter notebooks for exploration
├── data/               # Database and cache
└── logs/               # Application logs
```

### How It Works

1. **User Query:** You ask a question in natural language (e.g., "Should I buy Apple stock?")
2. **Agent Reasoning:** The LLM analyzes your query and decides which tools to use
3. **Tool Execution:** The agent automatically calls relevant tools (fetch data, calculate indicators)
4. **Analysis:** The agent processes all tool outputs
5. **Response:** You receive a comprehensive, actionable answer

## Features

### Stock Market Data
- Historical OHLCV (Open, High, Low, Close, Volume) data
- Real-time price quotes (15-minute delayed)
- Company information (sector, industry, market cap, P/E ratios)
- Multi-ticker batch quotes

### Technical Analysis
- **Momentum Indicators:** RSI, Stochastic Oscillator
- **Trend Indicators:** MACD, EMA (12, 26), SMA (20, 50, 200)
- **Volatility Indicators:** Bollinger Bands, ATR, Historical Volatility
- **Chart Patterns:** Support/Resistance level detection
- **Signals:** Automated buy/sell/hold signals based on indicators

### Risk Analysis
- Daily and annualized volatility
- Beta coefficient
- Average True Range (ATR)
- Risk level classification (LOW/MEDIUM/HIGH)

### AI-Powered Features
- Natural language query understanding
- Multi-tool orchestration
- Contextual analysis and recommendations
- Comparative analysis across multiple stocks
- Portfolio monitoring and alerts

## Installation

### Prerequisites

- Python 3.9 or higher
- pip package manager
- HuggingFace account (free) - [Sign up here](https://huggingface.co/join)
- Internet connection

### Step-by-Step Setup

1. **Clone the repository:**
   ```bash
   cd /path/to/financial-agent
   ```

2. **Create a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Linux/Mac
   # or
   venv\Scripts\activate  # Windows
   ```

3. **Install dependencies:**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**

   Get your HuggingFace API token:
   - Go to [HuggingFace Settings](https://huggingface.co/settings/tokens)
   - Create a new token (Type: Read)
   - Copy the token

   Edit the `.env` file:
   ```bash
   nano .env  # or use any text editor
   ```

   Add your token:
   ```
   HF_TOKEN=your_token_here
   ```

5. **Verify installation:**
   ```bash
   make test-quick
   ```

For detailed installation instructions, see [SETUP.md](SETUP.md).

## Quick Start

### Option 1: Web UI (Recommended for Beginners)

The easiest way to get started is using the web-based UI:

```bash
# Launch the web interface
make ui

# Or alternatively
python run_ui.py
```

Then open your browser to `http://localhost:7860`

**Features:**
- Natural language chat interface
- Interactive stock charts with technical indicators
- Multi-stock comparison view
- Portfolio monitoring dashboard
- No coding required!

For detailed UI instructions, see [UI_GUIDE.md](UI_GUIDE.md).

### Option 2: Python API

For programmatic access and scripting:

```python
from src.agents.financial_agent import create_agent

# Create the agent
agent = create_agent()

# Ask a simple question
result = agent.run("What is the current price of Apple (AAPL)?")
print(result)
```

### Comprehensive Stock Analysis

```python
# Analyze a stock with technical indicators
result = agent.analyze_stock("AAPL")
print(result)
```

### Compare Multiple Stocks

```python
# Compare stocks side-by-side
result = agent.compare_stocks(["AAPL", "GOOGL", "MSFT"])
print(result)
```

### Custom Natural Language Queries

```python
# Ask complex questions in plain English
query = """
Is Tesla oversold right now? What do the technical indicators suggest?
Should I buy, sell, or hold?
"""
result = agent.run(query)
print(result)
```

### Get Trading Signals

```python
# Get specific entry/exit recommendations
result = agent.get_trading_signals("TSLA")
print(result)
```

## Web UI

The Financial Agent includes a modern web interface built with Gradio, providing an intuitive way to interact with the AI agent without writing code.

### Launching the UI

```bash
# Using make (recommended)
make ui

# Using Python directly
python run_ui.py
```

Access the UI at: `http://localhost:7860`

### UI Features

#### 1. Chat Assistant
- Natural language interface for asking questions about stocks
- Conversational AI that understands context
- Automatic tool orchestration based on your query
- No need to know technical jargon

**Example queries:**
- "What's the current price of Apple?"
- "Should I buy Tesla based on technical indicators?"
- "Compare Microsoft and Google"

#### 2. Stock Dashboard
- Interactive candlestick charts with OHLC data
- Real-time technical indicators overlays (Moving Averages, Bollinger Bands)
- Separate indicators panel (RSI, MACD with signals)
- Comprehensive analysis summary
- Detailed technical data breakdown

**Features:**
- Zoom, pan, and hover for detailed values
- Customizable time periods (1mo, 3mo, 6mo, 1y, 2y)
- Support/resistance levels
- Risk and volatility metrics

#### 3. Stock Comparison
- Side-by-side comparison of multiple stocks
- Performance visualization (normalized returns)
- Comparison table with key metrics
- Perfect for portfolio selection

**Use cases:**
- Compare stocks in the same sector
- Find best risk/reward profiles
- Identify relative strength

#### 4. Portfolio Monitor
- Track multiple stocks simultaneously
- Real-time alerts for technical signals
- Performance dashboard
- Alert notifications for:
  - RSI overbought/oversold
  - MACD crossovers
  - Golden/Death crosses

### UI Screenshots and Workflow

**Typical workflow:**
1. Start with **Chat Assistant** for quick questions
2. Deep dive using **Stock Dashboard** for detailed analysis
3. Use **Comparison** to evaluate alternatives
4. Set up **Portfolio Monitor** to track your picks

### Customization

The UI is fully customizable. Edit `src/ui/gradio_app.py` to:
- Add new tabs
- Customize chart styles
- Add custom indicators
- Change themes and colors

### Deployment Options

**Local Access:**
```bash
# Default - localhost only
make ui
```

**Network Access:**
```python
# Edit run_ui.py
ui.launch(server_name="0.0.0.0")  # Already configured
# Access from other devices: http://YOUR_IP:7860
```

**Public Sharing:**
```python
# Edit run_ui.py
ui.launch(share=True)  # Creates public URL (72-hour expiry)
```

### UI Documentation

For a complete UI guide with screenshots and detailed instructions, see [UI_GUIDE.md](UI_GUIDE.md).

## Core Components

### 1. Financial Agent (`src/agents/financial_agent.py`)

The `FinancialAgent` class is the brain of the system. It orchestrates tool usage based on natural language input.

**Key Concepts:**

- **Code Agent:** Uses HuggingFace's `CodeAgent` which can write and execute Python code to solve tasks
- **Tool Registry:** Automatically discovers and registers all available tools
- **Reasoning:** The LLM decides which tools to use and in what order
- **Max Steps:** Limits the number of reasoning steps to prevent infinite loops

**Main Methods:**

```python
agent.run(task: str) -> str
# General-purpose method for any natural language task

agent.analyze_stock(ticker: str) -> str
# Performs comprehensive analysis of a single stock

agent.compare_stocks(tickers: List[str]) -> str
# Compares multiple stocks side-by-side

agent.get_trading_signals(ticker: str) -> str
# Returns specific trading recommendations

agent.monitor_portfolio(tickers: List[str]) -> str
# Monitors a portfolio and generates alerts
```

### 2. Market Data Tools (`src/tools/market_data.py`)

Tools for fetching financial data from Yahoo Finance.

#### `fetch_stock_data(ticker, period, interval)`
Retrieves historical OHLCV data and calculates basic statistics.

**Parameters:**
- `ticker` (str): Stock symbol (e.g., "AAPL", "TSLA")
- `period` (str): Time range (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)
- `interval` (str): Data granularity (1m, 5m, 15m, 30m, 1h, 1d, 1wk, 1mo)

**Returns:** JSON with:
- Current price and change percentage
- Volume statistics
- 52-week high/low
- Latest OHLCV data point

**Example:**
```python
from src.tools.market_data import fetch_stock_data
data = fetch_stock_data("AAPL", period="1mo", interval="1d")
```

#### `get_stock_info(ticker)`
Fetches detailed company information and fundamental metrics.

**Returns:**
- Company name, sector, industry
- Market cap, enterprise value
- P/E ratios, PEG ratio, price-to-book
- Dividend yield
- Business description

#### `get_multiple_quotes(tickers)`
Batch retrieves current quotes for multiple stocks.

**Parameters:**
- `tickers` (str): Comma-separated ticker symbols (e.g., "AAPL,GOOGL,MSFT")

**Returns:** Array of price quotes with change percentages

### 3. Technical Analysis Tools (`src/tools/technical_analysis.py`)

Tools for calculating technical indicators and generating signals.

#### `calculate_technical_indicators(ticker, period)`
Calculates comprehensive technical indicators.

**Indicators Calculated:**
- **RSI (Relative Strength Index):** Measures momentum (0-100)
  - < 30: Oversold (potential buy signal)
  - > 70: Overbought (potential sell signal)

- **MACD (Moving Average Convergence Divergence):**
  - MACD line, Signal line, Histogram
  - Crossovers indicate trend changes

- **Moving Averages:**
  - SMA: 20-day, 50-day, 200-day
  - EMA: 12-day, 26-day
  - Golden Cross (SMA50 > SMA200): Bullish
  - Death Cross (SMA50 < SMA200): Bearish

- **Bollinger Bands:** Volatility bands around price
  - Price near upper band: Potential reversal down
  - Price near lower band: Potential reversal up

- **Stochastic Oscillator:** Momentum indicator
  - < 20: Oversold
  - > 80: Overbought

**Returns:** JSON with:
- All indicator values
- Trading signals (booleans for each condition)
- Overall trend assessment (BULLISH/BEARISH/NEUTRAL)

#### `detect_support_resistance(ticker, period)`
Identifies key support and resistance price levels using local extrema detection.

**Algorithm:**
- Finds local minima (support levels) using scipy's `argrelextrema`
- Finds local maxima (resistance levels)
- Calculates distance from current price to nearest levels

**Returns:**
- Nearest support and resistance
- Top 3 support levels
- Top 3 resistance levels
- Distance percentages to key levels

**Use Case:** Entry/exit planning, stop-loss placement

#### `calculate_volatility(ticker, period)`
Calculates risk and volatility metrics.

**Metrics:**
- **Daily Volatility:** Standard deviation of daily returns
- **Annual Volatility:** Annualized standard deviation (× √252)
- **ATR (Average True Range):** Measures price volatility
- **Beta:** Correlation with market (S&P 500)
  - Beta > 1: More volatile than market
  - Beta < 1: Less volatile than market
- **Risk Level:** LOW/MEDIUM/HIGH classification

### 4. Configuration (`src/config/settings.py`)

Centralized configuration using Pydantic settings and environment variables.

**Key Settings:**
```python
HF_TOKEN           # HuggingFace API token (required)
HF_MODEL           # Model ID (default: meta-llama/Llama-3.1-8B-Instruct)
MAX_STEPS          # Max reasoning steps for agent (default: 10)
DATABASE_URL       # SQLite database path
DATA_DIR           # Directory for data storage
LOGS_DIR           # Directory for logs
```

### 5. Logger (`src/utils/logger.py`)

Structured logging with loguru for debugging and monitoring.

**Features:**
- Color-coded console output
- File rotation (prevents large log files)
- Multiple log levels (DEBUG, INFO, WARNING, ERROR)
- Automatic timestamping

## Usage Examples

### Example 1: Quick Price Check

```python
from src.agents.financial_agent import create_agent

agent = create_agent()
result = agent.run("What's the current price of Microsoft?")
print(result)
```

### Example 2: Deep Technical Analysis

```python
# Get comprehensive analysis with all indicators
result = agent.run("""
Analyze NVIDIA (NVDA) and provide:
1. Current price and trend
2. RSI and MACD indicators
3. Support and resistance levels
4. Volatility analysis
5. Your recommendation with reasoning
""")
print(result)
```

### Example 3: Compare Tech Stocks

```python
# Compare multiple stocks
result = agent.compare_stocks(["AAPL", "MSFT", "GOOGL", "AMZN", "META"])
print(result)
```

### Example 4: Portfolio Monitoring

```python
# Monitor your portfolio
portfolio = ["AAPL", "TSLA", "NVDA", "AMD", "PLTR"]
result = agent.monitor_portfolio(portfolio)
print(result)
```

### Example 5: Find Trading Opportunities

```python
# Get specific entry/exit points
result = agent.get_trading_signals("AAPL")
print(result)
```

### Example 6: Custom Analysis Script

```python
from src.agents.financial_agent import create_agent
from src.utils.logger import log

def analyze_momentum_stocks():
    """Find stocks with strong momentum signals."""
    agent = create_agent(verbose=True)

    tickers = ["AAPL", "GOOGL", "MSFT", "AMZN", "NVDA", "TSLA"]

    for ticker in tickers:
        log.info(f"Analyzing {ticker}...")
        result = agent.run(f"""
        For {ticker}, check if:
        1. RSI is between 40-60 (not extreme)
        2. MACD shows bullish crossover
        3. Price is above 50-day moving average

        If all conditions are met, this is a momentum buy candidate.
        """)
        print(f"\n{ticker} Analysis:\n{result}\n")

if __name__ == "__main__":
    analyze_momentum_stocks()
```

## Configuration

### Environment Variables

Create a `.env` file with the following variables:

```bash
# Required
HF_TOKEN=your_huggingface_token_here

# Optional - Model Configuration
HF_MODEL=meta-llama/Llama-3.1-8B-Instruct
MAX_STEPS=10

# Optional - Database
DATABASE_URL=sqlite:///./data/financial_agent.db

# Optional - Alerts (for future features)
TELEGRAM_BOT_TOKEN=
TELEGRAM_CHAT_ID=
SMTP_SERVER=
SMTP_PORT=
SMTP_EMAIL=
SMTP_PASSWORD=
```

### Using Alternative Models

You can use different HuggingFace models:

```python
# In your code
agent = create_agent(model_id="mistralai/Mistral-7B-Instruct-v0.3")

# Or in .env file
HF_MODEL=HuggingFaceH4/zephyr-7b-beta
```

### Using Local Models (Ollama)

To avoid API rate limits, run models locally with Ollama:

1. Install Ollama: `curl -fsSL https://ollama.com/install.sh | sh`
2. Pull a model: `ollama pull llama3.1:8b`
3. Modify `src/agents/financial_agent.py`:

```python
from smolagents import LiteLLMModel
model = LiteLLMModel(model_id="ollama/llama3.1:8b")
```

## Development

### Project Structure Explained

```
financial-agent/
├── src/
│   ├── __init__.py              # Package initialization
│   ├── agents/
│   │   ├── __init__.py
│   │   └── financial_agent.py   # Main AI agent logic
│   ├── tools/
│   │   ├── __init__.py          # Tool registry (imports all tools)
│   │   ├── market_data.py       # 3 tools for data fetching
│   │   └── technical_analysis.py # 3 tools for analysis
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py          # Configuration management
│   └── utils/
│       ├── __init__.py
│       └── logger.py            # Logging utilities
├── tests/
│   ├── __init__.py
│   └── test_tools.py            # Unit tests for tools
├── examples/
│   └── basic_usage.py           # Example scripts
├── notebooks/
│   └── exploration.ipynb        # Jupyter notebook for experiments
├── data/                        # SQLite database storage
├── logs/                        # Application logs
├── .env                         # Environment variables (git-ignored)
├── .env.example                 # Template for environment variables
├── .gitignore                   # Git ignore rules
├── requirements.txt             # Python dependencies
├── Makefile                     # Development commands
├── README.md                    # This file
├── SETUP.md                     # Detailed setup instructions
├── QUICKSTART.md                # Quick start guide
└── PROJECT_SUMMARY.md           # Project overview (French)
```

### Adding New Tools

Tools are functions decorated with `@tool` that the agent can call.

**Example - Create a new tool:**

```python
# src/tools/my_new_tool.py
from smolagents import tool
from src.utils.logger import log

@tool
def calculate_fibonacci_levels(ticker: str, period: str = "1y") -> str:
    """
    Calculates Fibonacci retracement levels for a stock.

    Args:
        ticker: Stock symbol
        period: Time period for high/low calculation

    Returns:
        JSON string with Fibonacci levels
    """
    try:
        # Your implementation here
        log.info(f"Calculating Fibonacci levels for {ticker}")

        # ... calculation logic ...

        result = {
            "ticker": ticker,
            "levels": {
                "0.0": 100.0,
                "23.6": 95.0,
                "38.2": 90.0,
                "50.0": 85.0,
                "61.8": 80.0,
                "100.0": 70.0
            }
        }

        return json.dumps(result, indent=2)

    except Exception as e:
        log.error(f"Error calculating Fibonacci: {str(e)}")
        return json.dumps({"error": str(e)})
```

**Register the tool:**

```python
# src/tools/__init__.py
from src.tools.market_data import fetch_stock_data, get_stock_info, get_multiple_quotes
from src.tools.technical_analysis import calculate_technical_indicators, detect_support_resistance, calculate_volatility
from src.tools.my_new_tool import calculate_fibonacci_levels

ALL_TOOLS = [
    fetch_stock_data,
    get_stock_info,
    get_multiple_quotes,
    calculate_technical_indicators,
    detect_support_resistance,
    calculate_volatility,
    calculate_fibonacci_levels,  # Add your new tool
]
```

### Makefile Commands

```bash
make help          # Show all available commands
make setup         # Create virtual environment
make install       # Install dependencies
make test          # Run all tests
make test-quick    # Quick smoke test
make run-example   # Run basic usage example
make notebook      # Start Jupyter notebook
make clean         # Clean cache and logs
make lint          # Run code linter
make format        # Format code with black
make check-env     # Verify .env configuration
make status        # Show project statistics
```

## Testing

### Run All Tests

```bash
make test
```

### Quick Smoke Test

```bash
make test-quick
```

### Manual Testing

```python
# Test market data tool directly
from src.tools.market_data import fetch_stock_data
import json

result = fetch_stock_data("AAPL", "5d")
data = json.loads(result)
print(f"Price: ${data['current_price']} ({data['change_percent']:+.2f}%)")
```

### Test Individual Tools

```python
from src.tools.technical_analysis import calculate_technical_indicators
import json

result = calculate_technical_indicators("AAPL", "3mo")
data = json.loads(result)
print(f"RSI: {data['indicators']['RSI']}")
print(f"Trend: {data['overall_trend']}")
```

## Limitations

### Current Limitations

1. **Data Delay:** Yahoo Finance data has a ~15-minute delay (not true real-time)
2. **Rate Limits:**
   - HuggingFace free tier has rate limits (~few requests/minute)
   - Yahoo Finance has rate limits for excessive requests
3. **Market Coverage:** Currently supports stocks only (no forex, crypto, or options)
4. **US Markets:** Primarily optimized for US stock tickers
5. **No Backtesting:** Cannot test strategies on historical data (yet)
6. **No Real Trading:** This is analysis-only; no broker integration

### Technical Limitations

- LLM reasoning quality depends on model size (8B parameters)
- Tool execution is sequential (no parallel tool calls yet)
- No persistent memory across sessions
- Limited to public market data (no proprietary data sources)

## Future Enhancements

### Planned Features (Phase 2)

- **Sentiment Analysis:**
  - News scraping and analysis
  - Social media sentiment (Reddit, Twitter)
  - Integration with FinBERT model

- **Chart Pattern Recognition:**
  - Head & Shoulders, Double Top/Bottom
  - Triangles, Flags, Pennants
  - Candlestick patterns

- **Database & Caching:**
  - SQLite for historical data storage
  - Redis cache for faster repeated queries
  - Alert management system

### Advanced Features (Phase 3)

- **Backtesting Framework:**
  - Test trading strategies on historical data
  - Performance metrics (Sharpe ratio, max drawdown)
  - Strategy optimization

- **Machine Learning Models:**
  - Price prediction models
  - Trend classification
  - Anomaly detection

- **Web Dashboard:**
  - FastAPI backend
  - React/Vue.js frontend
  - Interactive charts with Plotly
  - Real-time portfolio tracking

- **Alerts & Notifications:**
  - Telegram bot integration
  - Email alerts
  - Webhook support
  - Custom alert conditions

### Possible Extensions

- Cryptocurrency support (via Binance, Coinbase APIs)
- Forex support (via OANDA, Alpha Vantage)
- Options analysis and Greeks calculation
- Fundamental analysis tools (earnings, balance sheets)
- Multi-language support

## Contributing

Contributions are welcome! Here's how to contribute:

1. **Fork the repository**
2. **Create a feature branch:** `git checkout -b feature/new-tool`
3. **Make your changes** and add tests
4. **Format your code:** `make format`
5. **Run tests:** `make test`
6. **Commit:** `git commit -am 'Add new feature'`
7. **Push:** `git push origin feature/new-tool`
8. **Create a Pull Request**

### Code Style

- Follow PEP 8 guidelines
- Use type hints for function signatures
- Add docstrings to all functions and classes
- Keep functions focused and modular
- Add unit tests for new features

## Learning Resources

This project helps you learn:

1. **AI Agent Development:** Understanding how LLMs orchestrate tools
2. **Financial Analysis:** Technical indicators and trading strategies
3. **API Integration:** Working with financial data APIs
4. **Python Best Practices:** Project structure, testing, logging
5. **Async Programming:** Handling concurrent data fetching

### Recommended Reading

- [smolagents Documentation](https://huggingface.co/docs/smolagents)
- [Technical Analysis Basics](https://www.investopedia.com/technical-analysis-4689657)
- [Yahoo Finance API Guide](https://github.com/ranaroussi/yfinance)
- [LangChain Agents](https://python.langchain.com/docs/modules/agents/) (similar concepts)

## License

This project is open-source and available under the MIT License.

## Support

For issues, questions, or contributions:

- Open an issue on GitHub
- Check existing documentation (SETUP.md, QUICKSTART.md)
- Review the logs in `logs/financial_agent.log`

## Acknowledgments

- Built with [smolagents](https://github.com/huggingface/smolagents) by HuggingFace
- Financial data provided by [yfinance](https://github.com/ranaroussi/yfinance)
- Technical analysis powered by [ta](https://github.com/bukosabino/ta)
- LLM: Meta Llama 3.1 8B Instruct

---

**Disclaimer:** This tool is for educational and research purposes only. It is NOT financial advice. Always do your own research and consult with a licensed financial advisor before making investment decisions. Past performance does not guarantee future results.
