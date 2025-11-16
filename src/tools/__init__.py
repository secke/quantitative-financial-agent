"""Central registry of all available tools for the Financial Agent."""

from src.tools.market_data import (
    fetch_stock_data,
    get_stock_info,
    get_multiple_quotes,
)

from src.tools.technical_analysis import (
    calculate_technical_indicators,
    detect_support_resistance,
    calculate_volatility,
)

# List of all available tools
ALL_TOOLS = [
    # Market Data Tools
    fetch_stock_data,
    get_stock_info,
    get_multiple_quotes,
    
    # Technical Analysis Tools
    calculate_technical_indicators,
    detect_support_resistance,
    calculate_volatility,
]

# Categorized tools
MARKET_DATA_TOOLS = [
    fetch_stock_data,
    get_stock_info,
    get_multiple_quotes,
]

TECHNICAL_ANALYSIS_TOOLS = [
    calculate_technical_indicators,
    detect_support_resistance,
    calculate_volatility,
]
