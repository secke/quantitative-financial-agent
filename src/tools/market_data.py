"""Tools for fetching market data from various sources."""

import json
from typing import Optional
import yfinance as yf
import pandas as pd
from smolagents import tool
from src.utils.logger import log

@tool
def fetch_stock_data(ticker: str, period: str = "1mo", interval: str = "1d") -> str:
    """
    Fetches historical stock data for a given ticker symbol.
    
    Args:
        ticker: Stock symbol (e.g., 'AAPL', 'TSLA', 'GOOGL')
        period: Time period - valid periods: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max
        interval: Data interval - valid intervals: 1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo
    
    Returns:
        JSON string with OHLCV data and basic statistics
    """
    try:
        log.info(f"Fetching data for {ticker} with period={period}, interval={interval}")
        
        # Fetch data
        stock = yf.Ticker(ticker)
        df = stock.history(period=period, interval=interval)
        
        if df.empty:
            return json.dumps({
                "error": f"No data found for ticker {ticker}",
                "ticker": ticker
            })
        
        # Calculate basic statistics
        current_price = float(df['Close'].iloc[-1])
        prev_close = float(df['Close'].iloc[-2]) if len(df) > 1 else current_price
        change = current_price - prev_close
        change_pct = (change / prev_close) * 100 if prev_close != 0 else 0
        
        volume_avg = float(df['Volume'].mean())
        high_52w = float(df['High'].max())
        low_52w = float(df['Low'].min())
        
        result = {
            "ticker": ticker,
            "period": period,
            "interval": interval,
            "current_price": round(current_price, 2),
            "previous_close": round(prev_close, 2),
            "change": round(change, 2),
            "change_percent": round(change_pct, 2),
            "volume": int(df['Volume'].iloc[-1]),
            "average_volume": int(volume_avg),
            "high_52w": round(high_52w, 2),
            "low_52w": round(low_52w, 2),
            "data_points": len(df),
            "latest_data": {
                "date": df.index[-1].strftime("%Y-%m-%d"),
                "open": round(float(df['Open'].iloc[-1]), 2),
                "high": round(float(df['High'].iloc[-1]), 2),
                "low": round(float(df['Low'].iloc[-1]), 2),
                "close": round(float(df['Close'].iloc[-1]), 2),
                "volume": int(df['Volume'].iloc[-1])
            }
        }
        
        log.info(f"Successfully fetched data for {ticker}: ${current_price} ({change_pct:+.2f}%)")
        return json.dumps(result, indent=2)
        
    except Exception as e:
        log.error(f"Error fetching data for {ticker}: {str(e)}")
        return json.dumps({
            "error": str(e),
            "ticker": ticker
        })

@tool
def get_stock_info(ticker: str) -> str:
    """
    Gets detailed company information for a stock ticker.
    
    Args:
        ticker: Stock symbol (e.g., 'AAPL', 'TSLA')
    
    Returns:
        JSON string with company information (name, sector, industry, market cap, etc.)
    """
    try:
        log.info(f"Fetching info for {ticker}")
        
        stock = yf.Ticker(ticker)
        info = stock.info
        
        # Extract relevant information
        result = {
            "ticker": ticker,
            "name": info.get("longName", "N/A"),
            "sector": info.get("sector", "N/A"),
            "industry": info.get("industry", "N/A"),
            "country": info.get("country", "N/A"),
            "website": info.get("website", "N/A"),
            "market_cap": info.get("marketCap", 0),
            "enterprise_value": info.get("enterpriseValue", 0),
            "pe_ratio": info.get("trailingPE", 0),
            "forward_pe": info.get("forwardPE", 0),
            "peg_ratio": info.get("pegRatio", 0),
            "price_to_book": info.get("priceToBook", 0),
            "dividend_yield": info.get("dividendYield", 0),
            "52w_high": info.get("fiftyTwoWeekHigh", 0),
            "52w_low": info.get("fiftyTwoWeekLow", 0),
            "avg_volume": info.get("averageVolume", 0),
            "description": info.get("longBusinessSummary", "N/A")[:300] + "..."  # Truncate
        }
        
        log.info(f"Successfully fetched info for {ticker}: {result['name']}")
        return json.dumps(result, indent=2)
        
    except Exception as e:
        log.error(f"Error fetching info for {ticker}: {str(e)}")
        return json.dumps({
            "error": str(e),
            "ticker": ticker
        })

@tool  
def get_multiple_quotes(tickers: str) -> str:
    """
    Gets current quotes for multiple stock tickers.
    
    Args:
        tickers: Comma-separated list of ticker symbols (e.g., 'AAPL,GOOGL,MSFT')
    
    Returns:
        JSON string with current quotes for all tickers
    """
    try:
        ticker_list = [t.strip().upper() for t in tickers.split(",")]
        log.info(f"Fetching quotes for {len(ticker_list)} tickers")
        
        results = []
        for ticker in ticker_list:
            try:
                stock = yf.Ticker(ticker)
                hist = stock.history(period="5d")
                
                if not hist.empty:
                    current = float(hist['Close'].iloc[-1])
                    prev = float(hist['Close'].iloc[-2]) if len(hist) > 1 else current
                    change_pct = ((current - prev) / prev * 100) if prev != 0 else 0
                    
                    results.append({
                        "ticker": ticker,
                        "price": round(current, 2),
                        "change_percent": round(change_pct, 2),
                        "volume": int(hist['Volume'].iloc[-1])
                    })
            except Exception as e:
                results.append({
                    "ticker": ticker,
                    "error": str(e)
                })
        
        log.info(f"Successfully fetched {len(results)} quotes")
        return json.dumps(results, indent=2)
        
    except Exception as e:
        log.error(f"Error fetching multiple quotes: {str(e)}")
        return json.dumps({"error": str(e)})
