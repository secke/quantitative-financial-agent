"""Tools for technical analysis of stock data."""

import json
import yfinance as yf
import pandas as pd
import ta
from smolagents import tool
from src.utils.logger import log

@tool
def calculate_technical_indicators(ticker: str, period: str = "3mo") -> str:
    """
    Calculates key technical indicators for a stock.
    
    Args:
        ticker: Stock symbol (e.g., 'AAPL', 'TSLA')
        period: Time period for analysis (1mo, 3mo, 6mo, 1y)
    
    Returns:
        JSON string with RSI, MACD, Moving Averages, Bollinger Bands and trading signals
    """
    try:
        log.info(f"Calculating technical indicators for {ticker}")
        
        # Fetch data
        stock = yf.Ticker(ticker)
        df = stock.history(period=period)
        
        if df.empty:
            return json.dumps({"error": f"No data found for {ticker}"})
        
        # RSI (Relative Strength Index)
        rsi_indicator = ta.momentum.RSIIndicator(df['Close'], window=14)
        df['RSI'] = rsi_indicator.rsi()
        
        # MACD
        macd_indicator = ta.trend.MACD(df['Close'])
        df['MACD'] = macd_indicator.macd()
        df['MACD_signal'] = macd_indicator.macd_signal()
        df['MACD_diff'] = macd_indicator.macd_diff()
        
        # Moving Averages
        df['SMA_20'] = ta.trend.SMAIndicator(df['Close'], window=20).sma_indicator()
        df['SMA_50'] = ta.trend.SMAIndicator(df['Close'], window=50).sma_indicator()
        df['SMA_200'] = ta.trend.SMAIndicator(df['Close'], window=200).sma_indicator()
        df['EMA_12'] = ta.trend.EMAIndicator(df['Close'], window=12).ema_indicator()
        df['EMA_26'] = ta.trend.EMAIndicator(df['Close'], window=26).ema_indicator()
        
        # Bollinger Bands
        bollinger = ta.volatility.BollingerBands(df['Close'])
        df['BB_upper'] = bollinger.bollinger_hband()
        df['BB_middle'] = bollinger.bollinger_mavg()
        df['BB_lower'] = bollinger.bollinger_lband()
        
        # Stochastic Oscillator
        stoch = ta.momentum.StochasticOscillator(df['High'], df['Low'], df['Close'])
        df['Stoch_k'] = stoch.stoch()
        df['Stoch_d'] = stoch.stoch_signal()
        
        # Get latest values
        latest = df.iloc[-1]
        current_price = float(latest['Close'])
        
        # Generate signals
        signals = {
            # RSI Signals
            "rsi_oversold": latest['RSI'] < 30,
            "rsi_overbought": latest['RSI'] > 70,
            "rsi_neutral": 30 <= latest['RSI'] <= 70,
            
            # MACD Signals
            "macd_bullish_crossover": latest['MACD'] > latest['MACD_signal'],
            "macd_bearish_crossover": latest['MACD'] < latest['MACD_signal'],
            
            # Moving Average Signals
            "price_above_sma20": current_price > latest['SMA_20'],
            "price_above_sma50": current_price > latest['SMA_50'],
            "price_above_sma200": current_price > latest['SMA_200'],
            "golden_cross": latest['SMA_50'] > latest['SMA_200'],  # Bullish
            "death_cross": latest['SMA_50'] < latest['SMA_200'],    # Bearish
            
            # Bollinger Bands Signals
            "near_upper_band": current_price >= latest['BB_upper'] * 0.98,
            "near_lower_band": current_price <= latest['BB_lower'] * 1.02,
            
            # Stochastic Signals
            "stoch_oversold": latest['Stoch_k'] < 20,
            "stoch_overbought": latest['Stoch_k'] > 80,
        }
        
        # Overall trend analysis
        trend = "BULLISH" if (
            signals['price_above_sma50'] and 
            signals['macd_bullish_crossover'] and 
            not signals['rsi_overbought']
        ) else "BEARISH" if (
            not signals['price_above_sma50'] and 
            signals['macd_bearish_crossover'] and 
            not signals['rsi_oversold']
        ) else "NEUTRAL"

        # convert numpy bool to regular python bool
        signals = {k: bool(v) for k, v in signals.items()}

        result = {
            "ticker": ticker,
            "current_price": round(current_price, 2),
            "date": df.index[-1].strftime("%Y-%m-%d"),
            "indicators": {
                "RSI": round(float(latest['RSI']), 2),
                "MACD": round(float(latest['MACD']), 4),
                "MACD_signal": round(float(latest['MACD_signal']), 4),
                "MACD_histogram": round(float(latest['MACD_diff']), 4),
                "SMA_20": round(float(latest['SMA_20']), 2),
                "SMA_50": round(float(latest['SMA_50']), 2),
                "SMA_200": round(float(latest['SMA_200']), 2),
                "EMA_12": round(float(latest['EMA_12']), 2),
                "EMA_26": round(float(latest['EMA_26']), 2),
                "BB_upper": round(float(latest['BB_upper']), 2),
                "BB_middle": round(float(latest['BB_middle']), 2),
                "BB_lower": round(float(latest['BB_lower']), 2),
                "Stochastic_K": round(float(latest['Stoch_k']), 2),
                "Stochastic_D": round(float(latest['Stoch_d']), 2),
            },
            "signals": signals,
            "overall_trend": trend
        }
        
        log.info(f"Technical analysis for {ticker}: {trend} trend, RSI={latest['RSI']:.1f}")
        # log.info(f"The result is: {result}")
        return json.dumps(result, indent=2)
        
    except Exception as e:
        log.error(f"Error calculating indicators for {ticker}: {str(e)}")
        return json.dumps({"error": str(e), "ticker": ticker})

@tool
def detect_support_resistance(ticker: str, period: str = "6mo") -> str:
    """
    Detects support and resistance levels using historical price data.
    
    Args:
        ticker: Stock symbol
        period: Time period for analysis
    
    Returns:
        JSON string with identified support and resistance levels
    """
    try:
        log.info(f"Detecting support/resistance for {ticker}")
        
        stock = yf.Ticker(ticker)
        df = stock.history(period=period)
        
        if df.empty:
            return json.dumps({"error": f"No data found for {ticker}"})
        
        # Find local maxima (resistance) and minima (support)
        from scipy.signal import argrelextrema
        import numpy as np
        
        # Convert to numpy array
        prices = df['Close'].values
        
        # Find local maxima (resistance levels)
        max_idx = argrelextrema(prices, np.greater, order=5)[0]
        resistance_levels = sorted([float(prices[i]) for i in max_idx], reverse=True)[:5]
        
        # Find local minima (support levels)
        min_idx = argrelextrema(prices, np.less, order=5)[0]
        support_levels = sorted([float(prices[i]) for i in min_idx])[:5]
        
        current_price = float(df['Close'].iloc[-1])
        
        # Find nearest support and resistance
        nearest_resistance = min([r for r in resistance_levels if r > current_price], default=None)
        nearest_support = max([s for s in support_levels if s < current_price], default=None)
        
        result = {
            "ticker": ticker,
            "current_price": round(current_price, 2),
            "nearest_resistance": round(nearest_resistance, 2) if nearest_resistance else None,
            "nearest_support": round(nearest_support, 2) if nearest_support else None,
            "resistance_levels": [round(r, 2) for r in resistance_levels[:3]],
            "support_levels": [round(s, 2) for s in support_levels[:3]],
            "distance_to_resistance": round(((nearest_resistance - current_price) / current_price * 100), 2) if nearest_resistance else None,
            "distance_to_support": round(((current_price - nearest_support) / current_price * 100), 2) if nearest_support else None,
        }
        
        log.info(f"Support/Resistance for {ticker}: Support=${nearest_support}, Resistance=${nearest_resistance}")
        return json.dumps(result, indent=2)
        
    except Exception as e:
        log.error(f"Error detecting support/resistance for {ticker}: {str(e)}")
        return json.dumps({"error": str(e), "ticker": ticker})

@tool
def calculate_volatility(ticker: str, period: str = "1y") -> str:
    """
    Calculates various volatility metrics for a stock.
    
    Args:
        ticker: Stock symbol
        period: Time period for analysis
    
    Returns:
        JSON string with volatility metrics (standard deviation, ATR, beta)
    """
    try:
        log.info(f"Calculating volatility for {ticker}")
        
        stock = yf.Ticker(ticker)
        df = stock.history(period=period)
        
        if df.empty:
            return json.dumps({"error": f"No data found for {ticker}"})
        
        # Calculate daily returns
        df['Returns'] = df['Close'].pct_change()
        
        # Historical volatility (annualized)
        daily_volatility = df['Returns'].std()
        annual_volatility = daily_volatility * (252 ** 0.5)  # 252 trading days
        
        # Average True Range (ATR)
        atr = ta.volatility.AverageTrueRange(df['High'], df['Low'], df['Close']).average_true_range()
        
        # Get info for beta
        info = stock.info
        beta = info.get('beta', None)
        
        result = {
            "ticker": ticker,
            "volatility_daily": round(float(daily_volatility * 100), 2),  # percentage
            "volatility_annual": round(float(annual_volatility * 100), 2),  # percentage
            "atr_current": round(float(atr.iloc[-1]), 2),
            "atr_avg": round(float(atr.mean()), 2),
            "beta": round(float(beta), 2) if beta else None,
            "risk_level": "HIGH" if annual_volatility > 0.4 else "MEDIUM" if annual_volatility > 0.2 else "LOW"
        }
        
        log.info(f"Volatility for {ticker}: {result['volatility_annual']:.2f}% annual, Risk={result['risk_level']}")
        return json.dumps(result, indent=2)
        
    except Exception as e:
        log.error(f"Error calculating volatility for {ticker}: {str(e)}")
        return json.dumps({"error": str(e), "ticker": ticker})
