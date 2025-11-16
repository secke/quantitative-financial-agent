"""Test script to verify tools are working correctly."""

import sys
# sys.path.insert(0, 'financial-agent')

from src.tools.market_data import fetch_stock_data, get_stock_info, get_multiple_quotes
from src.tools.technical_analysis import calculate_technical_indicators, detect_support_resistance, calculate_volatility
from src.utils.logger import log
import json

def test_market_data():
    """Test market data tools."""
    print("\n" + "="*60)
    print("TESTING MARKET DATA TOOLS")
    print("="*60)
    
    # Test 1: Fetch stock data
    print("\n1. Testing fetch_stock_data for AAPL...")
    result = fetch_stock_data("AAPL", "5d")
    data = json.loads(result)
    if "error" not in data:
        print(f"✓ SUCCESS: Current price = ${data['current_price']}")
        print(f"  Change: {data['change_percent']:+.2f}%")
    else:
        print(f"✗ ERROR: {data['error']}")
    
    # Test 2: Get stock info
    print("\n2. Testing get_stock_info for AAPL...")
    result = get_stock_info("AAPL")
    data = json.loads(result)
    if "error" not in data:
        print(f"✓ SUCCESS: {data['name']}")
        print(f"  Sector: {data['sector']}")
        print(f"  Market Cap: ${data['market_cap']:,.0f}")
    else:
        print(f"✗ ERROR: {data['error']}")
    
    # Test 3: Get multiple quotes
    print("\n3. Testing get_multiple_quotes...")
    result = get_multiple_quotes("AAPL,GOOGL,MSFT")
    data = json.loads(result)
    if isinstance(data, list):
        print(f"✓ SUCCESS: Fetched {len(data)} quotes")
        for quote in data:
            if "error" not in quote:
                print(f"  {quote['ticker']}: ${quote['price']} ({quote['change_percent']:+.2f}%)")
    else:
        print(f"✗ ERROR: {data.get('error', 'Unknown error')}")

def test_technical_analysis():
    """Test technical analysis tools."""
    print("\n" + "="*60)
    print("TESTING TECHNICAL ANALYSIS TOOLS")
    print("="*60)
    
    # Test 1: Calculate indicators
    print("\n1. Testing calculate_technical_indicators for AAPL...")
    result = calculate_technical_indicators("AAPL", "3mo")
    data = json.loads(result)
    if "error" not in data:
        print(f"✓ SUCCESS: {data['overall_trend']} trend")
        print(f"  RSI: {data['indicators']['RSI']}")
        print(f"  MACD: {data['indicators']['MACD']}")
        print(f"  Price vs SMA50: {'Above' if data['signals']['price_above_sma50'] else 'Below'}")
    else:
        print(f"✗ ERROR: {data['error']}")
    
    # Test 2: Support/Resistance
    print("\n2. Testing detect_support_resistance for AAPL...")
    result = detect_support_resistance("AAPL", "6mo")
    data = json.loads(result)
    if "error" not in data:
        print(f"✓ SUCCESS: Current price = ${data['current_price']}")
        if data['nearest_resistance']:
            print(f"  Nearest Resistance: ${data['nearest_resistance']} ({data['distance_to_resistance']:+.2f}%)")
        if data['nearest_support']:
            print(f"  Nearest Support: ${data['nearest_support']} ({data['distance_to_support']:+.2f}%)")
    else:
        print(f"✗ ERROR: {data['error']}")
    
    # Test 3: Volatility
    print("\n3. Testing calculate_volatility for AAPL...")
    result = calculate_volatility("AAPL", "1y")
    data = json.loads(result)
    if "error" not in data:
        print(f"✓ SUCCESS: Risk Level = {data['risk_level']}")
        print(f"  Annual Volatility: {data['volatility_annual']}%")
        print(f"  Beta: {data['beta']}")
    else:
        print(f"✗ ERROR: {data['error']}")

def main():
    """Run all tests."""
    print("\n" + "="*60)
    print("FINANCIAL AGENT - TOOLS TEST SUITE")
    print("="*60)
    
    try:
        test_market_data()
        test_technical_analysis()
        
        print("\n" + "="*60)
        print("ALL TESTS COMPLETED")
        print("="*60)
        
    except Exception as e:
        print(f"\n✗ FATAL ERROR: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
