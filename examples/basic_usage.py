"""Simple example usage of the Financial Agent."""

import sys
sys.path.insert(0, 'financial-agent')

from src.agents.financial_agent import create_agent
from src.utils.logger import log

def example_basic_analysis():
    """Example: Basic stock analysis."""
    print("\n" + "="*60)
    print("EXAMPLE 1: Basic Stock Analysis")
    print("="*60 + "\n")
    
    # Create agent
    agent = create_agent(verbose=False)
    
    # Simple analysis
    result = agent.run("What is the current price of Apple (AAPL)?")
    print(result)

def example_technical_analysis():
    """Example: Technical analysis with signals."""
    print("\n" + "="*60)
    print("EXAMPLE 2: Technical Analysis")
    print("="*60 + "\n")
    
    agent = create_agent(verbose=False)
    
    result = agent.analyze_stock("AAPL")
    print(result)

def example_comparison():
    """Example: Compare multiple stocks."""
    print("\n" + "="*60)
    print("EXAMPLE 3: Stock Comparison")
    print("="*60 + "\n")
    
    agent = create_agent(verbose=False)
    
    result = agent.compare_stocks(["AAPL", "GOOGL", "MSFT"])
    print(result)

def example_custom_query():
    """Example: Custom natural language query."""
    print("\n" + "="*60)
    print("EXAMPLE 4: Custom Query")
    print("="*60 + "\n")
    
    agent = create_agent(verbose=False)
    
    query = """
    I'm interested in Tesla (TSLA). Can you tell me:
    1. If the stock is currently overbought or oversold based on RSI
    2. What the MACD indicator suggests
    3. Whether it's near support or resistance levels
    4. Your overall recommendation
    """
    
    result = agent.run(query)
    print(result)

def main():
    """Run all examples."""
    print("\n" + "="*70)
    print("FINANCIAL AGENT - USAGE EXAMPLES")
    print("="*70)
    
    try:
        # Run examples one by one
        # Uncomment the ones you want to test
        
        example_basic_analysis()
        # example_technical_analysis()
        # example_comparison()
        # example_custom_query()
        
    except Exception as e:
        log.error(f"Error running example: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
