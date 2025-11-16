"""Main Financial Agent using smolagents framework."""

import os
from typing import List, Optional
from smolagents import CodeAgent, InferenceClientModel, ToolCallingAgent
from src.tools import ALL_TOOLS
from src.config.settings import settings
from src.utils.logger import log


class FinancialAgent:
    """
    AI Agent for financial analysis using open-source models.
    
    Capabilities:
    - Fetch market data (prices, volumes, company info)
    - Calculate technical indicators (RSI, MACD, Moving Averages)
    - Detect support/resistance levels
    - Analyze volatility and risk metrics
    - Generate trading signals and recommendations
    """
    
    def __init__(
        self,
        model_id: Optional[str] = None,
        tools: Optional[List] = None,
        max_steps: Optional[int] = None,
        verbose: bool = True,
    ):
        """
        Initialize the Financial Agent.
        
        Args:
            model_id: HuggingFace model ID (default from settings)
            tools: List of tools to use (default: ALL_TOOLS)
            max_steps: Maximum reasoning steps (default from settings)
            verbose: Whether to print agent reasoning
        """
        self.model_id = model_id or settings.HF_MODEL
        self.tools = tools or ALL_TOOLS
        self.max_steps = max_steps or settings.MAX_STEPS
        self.verbose = verbose
        
        log.info(f"Initializing FinancialAgent with model: {self.model_id}")
        
        # Initialize the LLM
        self.model = self._init_model()
        
        # Initialize the agent
        self.agent = CodeAgent(
            tools=self.tools,
            model=self.model,
            max_steps=self.max_steps,
            # verbose=self.verbose,
        )
        
        log.info(f"FinancialAgent initialized with {len(self.tools)} tools")
    
    def _init_model(self):
        """Initialize the language model."""
        try:
            # Check if HF token is provided
            if settings.HF_TOKEN:
                os.environ["HF_TOKEN"] = settings.HF_TOKEN
            
            model = InferenceClientModel(model_id=self.model_id)
            log.info(f"Model {self.model_id} loaded successfully")
            return model
            
        except Exception as e:
            log.error(f"Error loading model: {str(e)}")
            raise
    
    def run(self, task: str) -> str:
        """
        Run the agent with a given task.
        
        Args:
            task: Natural language instruction for the agent
        
        Returns:
            Agent's response as a string
        """
        try:
            log.info(f"Running task: {task[:100]}...")
            result = self.agent.run(task)
            log.info("Task completed successfully")
            return result
            
        except Exception as e:
            error_msg = f"Error running task: {str(e)}"
            log.error(error_msg)
            return error_msg
    
    def analyze_stock(self, ticker: str) -> str:
        """
        Perform comprehensive analysis of a stock.
        
        Args:
            ticker: Stock symbol (e.g., 'AAPL')
        
        Returns:
            Comprehensive analysis report
        """
        task = f"""
        Perform a comprehensive analysis of {ticker} stock and provide:
        
        1. Current price and basic statistics
        2. Technical indicators (RSI, MACD, Moving Averages)
        3. Support and resistance levels
        4. Volatility analysis
        5. Trading signals based on technical indicators
        6. Overall recommendation (BUY/HOLD/SELL) with reasoning
        
        Format the response in a clear, structured manner.
        """
        return self.run(task)
    
    def compare_stocks(self, tickers: List[str]) -> str:
        """
        Compare multiple stocks side by side.
        
        Args:
            tickers: List of stock symbols
        
        Returns:
            Comparative analysis
        """
        tickers_str = ", ".join(tickers)
        task = f"""
        Compare the following stocks: {tickers_str}
        
        For each stock, provide:
        1. Current price and recent performance
        2. Key technical indicators
        3. Risk level (volatility)
        4. Trading signals
        
        Then provide a comparative summary highlighting:
        - Which stock shows the strongest bullish signals
        - Which stock has the best risk/reward profile
        - Overall recommendation for portfolio allocation
        """
        return self.run(task)
    
    def get_trading_signals(self, ticker: str) -> str:
        """
        Get specific trading signals for a stock.
        
        Args:
            ticker: Stock symbol
        
        Returns:
            Trading signals and entry/exit recommendations
        """
        task = f"""
        Analyze {ticker} and provide specific trading signals:
        
        1. Current trend (BULLISH/BEARISH/NEUTRAL)
        2. Entry points (if recommending BUY)
        3. Target price levels
        4. Stop loss recommendations
        5. Risk/reward ratio
        6. Timeframe for the trade (short/medium/long term)
        
        Base your analysis on technical indicators and support/resistance levels.
        """
        return self.run(task)
    
    def monitor_portfolio(self, tickers: List[str]) -> str:
        """
        Monitor a portfolio of stocks and generate alerts.
        
        Args:
            tickers: List of stock symbols in portfolio
        
        Returns:
            Portfolio monitoring report with alerts
        """
        tickers_str = ", ".join(tickers)
        task = f"""
        Monitor the following portfolio: {tickers_str}
        
        For each stock:
        1. Current price and change percentage
        2. Any technical indicator alerts (overbought/oversold, crossovers)
        3. Approaching support or resistance levels
        4. Unusual volume activity
        
        Provide a summary of:
        - Stocks requiring immediate attention
        - Overall portfolio health
        - Recommended actions
        """
        return self.run(task)


def create_agent(
    model_id: Optional[str] = None,
    verbose: bool = True,
) -> FinancialAgent:
    """
    Factory function to create a FinancialAgent instance.
    
    Args:
        model_id: HuggingFace model ID
        verbose: Whether to print agent reasoning
    
    Returns:
        Configured FinancialAgent instance
    """
    return FinancialAgent(model_id=model_id, verbose=verbose)
