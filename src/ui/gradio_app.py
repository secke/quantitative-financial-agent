"""Gradio UI for Financial Agent."""

import gradio as gr
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import json
import yfinance as yf
from typing import List, Tuple, Optional
from datetime import datetime

from src.agents.financial_agent import create_agent
from src.tools.market_data import fetch_stock_data, get_stock_info
from src.tools.technical_analysis import (
    calculate_technical_indicators,
    detect_support_resistance,
    calculate_volatility
)
from src.utils.logger import log


# Initialize agent globally
agent = None


def initialize_agent():
    """Initialize the financial agent."""
    global agent
    if agent is None:
        try:
            agent = create_agent(verbose=False)
            log.info("Financial agent initialized successfully")
            return True
        except Exception as e:
            log.error(f"Failed to initialize agent: {str(e)}")
            return False
    return True


def chat_with_agent(message: str, history: List[Tuple[str, str]]) -> str:
    """
    Chat interface for natural language queries.

    Args:
        message: User's message
        history: Chat history

    Returns:
        Agent's response
    """
    try:
        if not initialize_agent():
            return "Error: Failed to initialize agent. Please check your HF_TOKEN in .env file."

        log.info(f"User query: {message}")
        response = agent.run(message)
        log.info("Agent response generated")
        return response

    except Exception as e:
        error_msg = f"Error: {str(e)}"
        log.error(error_msg)
        return error_msg


def create_stock_chart(ticker: str, period: str = "3mo") -> go.Figure:
    """
    Create an interactive stock price chart with technical indicators.

    Args:
        ticker: Stock symbol
        period: Time period

    Returns:
        Plotly figure object
    """
    try:
        # Fetch data
        stock = yf.Ticker(ticker)
        df = stock.history(period=period)

        if df.empty:
            return None

        # Calculate indicators
        from ta.trend import SMAIndicator, EMAIndicator
        from ta.volatility import BollingerBands

        df['SMA_20'] = SMAIndicator(df['Close'], window=20).sma_indicator()
        df['SMA_50'] = SMAIndicator(df['Close'], window=50).sma_indicator()

        bollinger = BollingerBands(df['Close'])
        df['BB_upper'] = bollinger.bollinger_hband()
        df['BB_lower'] = bollinger.bollinger_lband()

        # Create subplots
        fig = make_subplots(
            rows=2, cols=1,
            shared_xaxes=True,
            vertical_spacing=0.03,
            row_heights=[0.7, 0.3],
            subplot_titles=(f'{ticker} Price Chart', 'Volume')
        )

        # Candlestick chart
        fig.add_trace(
            go.Candlestick(
                x=df.index,
                open=df['Open'],
                high=df['High'],
                low=df['Low'],
                close=df['Close'],
                name='Price'
            ),
            row=1, col=1
        )

        # Moving averages
        fig.add_trace(
            go.Scatter(
                x=df.index, y=df['SMA_20'],
                name='SMA 20',
                line=dict(color='orange', width=1)
            ),
            row=1, col=1
        )

        fig.add_trace(
            go.Scatter(
                x=df.index, y=df['SMA_50'],
                name='SMA 50',
                line=dict(color='blue', width=1)
            ),
            row=1, col=1
        )

        # Bollinger Bands
        fig.add_trace(
            go.Scatter(
                x=df.index, y=df['BB_upper'],
                name='BB Upper',
                line=dict(color='gray', width=1, dash='dash'),
                showlegend=False
            ),
            row=1, col=1
        )

        fig.add_trace(
            go.Scatter(
                x=df.index, y=df['BB_lower'],
                name='BB Lower',
                line=dict(color='gray', width=1, dash='dash'),
                fill='tonexty',
                fillcolor='rgba(128, 128, 128, 0.1)',
                showlegend=False
            ),
            row=1, col=1
        )

        # Volume bars
        colors = ['red' if df['Close'][i] < df['Open'][i] else 'green'
                  for i in range(len(df))]

        fig.add_trace(
            go.Bar(
                x=df.index, y=df['Volume'],
                name='Volume',
                marker_color=colors,
                showlegend=False
            ),
            row=2, col=1
        )

        # Update layout
        fig.update_layout(
            title=f'{ticker} Technical Analysis',
            yaxis_title='Price ($)',
            yaxis2_title='Volume',
            xaxis_rangeslider_visible=False,
            height=600,
            template='plotly_dark',
            hovermode='x unified'
        )

        return fig

    except Exception as e:
        log.error(f"Error creating chart for {ticker}: {str(e)}")
        return None


def create_indicators_chart(ticker: str, period: str = "3mo") -> go.Figure:
    """
    Create a chart showing technical indicators (RSI, MACD).

    Args:
        ticker: Stock symbol
        period: Time period

    Returns:
        Plotly figure object
    """
    try:
        stock = yf.Ticker(ticker)
        df = stock.history(period=period)

        if df.empty:
            return None

        from ta.momentum import RSIIndicator
        from ta.trend import MACD

        # Calculate indicators
        df['RSI'] = RSIIndicator(df['Close'], window=14).rsi()
        macd = MACD(df['Close'])
        df['MACD'] = macd.macd()
        df['MACD_signal'] = macd.macd_signal()
        df['MACD_diff'] = macd.macd_diff()

        # Create subplots
        fig = make_subplots(
            rows=2, cols=1,
            shared_xaxes=True,
            vertical_spacing=0.1,
            subplot_titles=('RSI (Relative Strength Index)', 'MACD'),
            row_heights=[0.5, 0.5]
        )

        # RSI
        fig.add_trace(
            go.Scatter(
                x=df.index, y=df['RSI'],
                name='RSI',
                line=dict(color='purple', width=2)
            ),
            row=1, col=1
        )

        # RSI levels
        fig.add_hline(y=70, line_dash="dash", line_color="red",
                      annotation_text="Overbought (70)", row=1, col=1)
        fig.add_hline(y=30, line_dash="dash", line_color="green",
                      annotation_text="Oversold (30)", row=1, col=1)

        # MACD
        fig.add_trace(
            go.Scatter(
                x=df.index, y=df['MACD'],
                name='MACD',
                line=dict(color='blue', width=2)
            ),
            row=2, col=1
        )

        fig.add_trace(
            go.Scatter(
                x=df.index, y=df['MACD_signal'],
                name='Signal',
                line=dict(color='orange', width=2)
            ),
            row=2, col=1
        )

        # MACD histogram
        colors = ['green' if val >= 0 else 'red' for val in df['MACD_diff']]
        fig.add_trace(
            go.Bar(
                x=df.index, y=df['MACD_diff'],
                name='Histogram',
                marker_color=colors
            ),
            row=2, col=1
        )

        # Update layout
        fig.update_layout(
            height=500,
            template='plotly_dark',
            showlegend=True,
            hovermode='x unified'
        )

        fig.update_yaxes(title_text="RSI", row=1, col=1)
        fig.update_yaxes(title_text="MACD", row=2, col=1)

        return fig

    except Exception as e:
        log.error(f"Error creating indicators chart: {str(e)}")
        return None


def analyze_stock(ticker: str, period: str = "3mo") -> Tuple[str, go.Figure, go.Figure, str]:
    """
    Comprehensive stock analysis for the dashboard.

    Args:
        ticker: Stock symbol
        period: Time period

    Returns:
        Tuple of (summary, price_chart, indicators_chart, technical_data)
    """
    try:
        ticker = ticker.upper().strip()

        # Get stock data
        data_json = fetch_stock_data(ticker, period)
        data = json.loads(data_json)

        if 'error' in data:
            return f"Error: {data['error']}", None, None, ""

        # Get technical indicators
        tech_json = calculate_technical_indicators(ticker, period)
        tech = json.loads(tech_json)

        # Get support/resistance
        sr_json = detect_support_resistance(ticker, "6mo")
        sr = json.loads(sr_json)

        # Get volatility
        vol_json = calculate_volatility(ticker, "1y")
        vol = json.loads(vol_json)

        # Create summary
        summary = f"""
## {ticker} Stock Analysis

### Current Price: ${data['current_price']} ({data['change_percent']:+.2f}%)

### Key Metrics:
- **52-Week High:** ${data['high_52w']}
- **52-Week Low:** ${data['low_52w']}
- **Volume:** {data['volume']:,}
- **Avg Volume:** {data['average_volume']:,}

### Technical Indicators:
- **RSI:** {tech['indicators']['RSI']:.2f} {'(Overbought)' if tech['indicators']['RSI'] > 70 else '(Oversold)' if tech['indicators']['RSI'] < 30 else '(Neutral)'}
- **MACD:** {tech['indicators']['MACD']:.4f} {'(Bullish)' if tech['signals']['macd_bullish_crossover'] else '(Bearish)'}
- **Trend:** {tech['overall_trend']}

### Support & Resistance:
- **Nearest Resistance:** ${sr.get('nearest_resistance', 'N/A')} ({sr.get('distance_to_resistance', 0):.2f}% away)
- **Nearest Support:** ${sr.get('nearest_support', 'N/A')} ({sr.get('distance_to_support', 0):.2f}% away)

### Risk Analysis:
- **Volatility (Annual):** {vol['volatility_annual']:.2f}%
- **Risk Level:** {vol['risk_level']}
- **Beta:** {vol.get('beta', 'N/A')}
"""

        # Create detailed technical data
        tech_details = f"""
### Detailed Technical Analysis

**Moving Averages:**
- SMA 20: ${tech['indicators']['SMA_20']:.2f}
- SMA 50: ${tech['indicators']['SMA_50']:.2f}
- SMA 200: ${tech['indicators']['SMA_200']:.2f}
- Price above SMA50: {'✓ Yes' if tech['signals']['price_above_sma50'] else '✗ No'}
- Price above SMA200: {'✓ Yes' if tech['signals']['price_above_sma200'] else '✗ No'}

**MACD Details:**
- MACD Line: {tech['indicators']['MACD']:.4f}
- Signal Line: {tech['indicators']['MACD_signal']:.4f}
- Histogram: {tech['indicators']['MACD_histogram']:.4f}

**Bollinger Bands:**
- Upper: ${tech['indicators']['BB_upper']:.2f}
- Middle: ${tech['indicators']['BB_middle']:.2f}
- Lower: ${tech['indicators']['BB_lower']:.2f}

**Stochastic Oscillator:**
- %K: {tech['indicators']['Stochastic_K']:.2f}
- %D: {tech['indicators']['Stochastic_D']:.2f}

**Trading Signals:**
- RSI Oversold: {'✓' if tech['signals']['rsi_oversold'] else '✗'}
- RSI Overbought: {'✓' if tech['signals']['rsi_overbought'] else '✗'}
- MACD Bullish Crossover: {'✓' if tech['signals']['macd_bullish_crossover'] else '✗'}
- Golden Cross: {'✓' if tech['signals']['golden_cross'] else '✗'}
- Death Cross: {'✓' if tech['signals']['death_cross'] else '✗'}
"""

        # Create charts
        price_chart = create_stock_chart(ticker, period)
        indicators_chart = create_indicators_chart(ticker, period)

        return summary, price_chart, indicators_chart, tech_details

    except Exception as e:
        error_msg = f"Error analyzing {ticker}: {str(e)}"
        log.error(error_msg)
        return error_msg, None, None, ""


def compare_stocks(tickers_input: str) -> Tuple[str, go.Figure]:
    """
    Compare multiple stocks side by side.

    Args:
        tickers_input: Comma-separated ticker symbols

    Returns:
        Tuple of (comparison_text, comparison_chart)
    """
    try:
        tickers = [t.strip().upper() for t in tickers_input.split(',')]

        if len(tickers) < 2:
            return "Please enter at least 2 tickers separated by commas", None

        comparison_data = []

        for ticker in tickers:
            try:
                # Get data
                data_json = fetch_stock_data(ticker, "1mo")
                data = json.loads(data_json)

                tech_json = calculate_technical_indicators(ticker, "3mo")
                tech = json.loads(tech_json)

                vol_json = calculate_volatility(ticker, "1y")
                vol = json.loads(vol_json)

                comparison_data.append({
                    'Ticker': ticker,
                    'Price': f"${data['current_price']}",
                    'Change %': f"{data['change_percent']:+.2f}%",
                    'RSI': f"{tech['indicators']['RSI']:.1f}",
                    'Trend': tech['overall_trend'],
                    'Volatility': f"{vol['volatility_annual']:.1f}%",
                    'Risk': vol['risk_level']
                })

            except Exception as e:
                log.error(f"Error fetching data for {ticker}: {str(e)}")
                continue

        # Create comparison table
        df = pd.DataFrame(comparison_data)
        comparison_text = "## Stock Comparison\n\n" + df.to_markdown(index=False)

        # Create performance comparison chart
        fig = go.Figure()

        for ticker in tickers:
            try:
                stock = yf.Ticker(ticker)
                hist = stock.history(period="3mo")

                if not hist.empty:
                    # Normalize to percentage change
                    normalized = (hist['Close'] / hist['Close'].iloc[0] - 1) * 100

                    fig.add_trace(
                        go.Scatter(
                            x=hist.index,
                            y=normalized,
                            name=ticker,
                            mode='lines'
                        )
                    )
            except Exception as e:
                log.error(f"Error creating chart for {ticker}: {str(e)}")
                continue

        fig.update_layout(
            title='3-Month Performance Comparison (Normalized)',
            yaxis_title='Return (%)',
            xaxis_title='Date',
            height=500,
            template='plotly_dark',
            hovermode='x unified'
        )

        return comparison_text, fig

    except Exception as e:
        error_msg = f"Error comparing stocks: {str(e)}"
        log.error(error_msg)
        return error_msg, None


def monitor_portfolio(tickers_input: str) -> Tuple[str, go.Figure]:
    """
    Monitor portfolio and generate alerts.

    Args:
        tickers_input: Comma-separated ticker symbols

    Returns:
        Tuple of (portfolio_summary, portfolio_chart)
    """
    try:
        tickers = [t.strip().upper() for t in tickers_input.split(',')]

        if len(tickers) < 1:
            return "Please enter at least 1 ticker", None

        portfolio_data = []
        alerts = []

        for ticker in tickers:
            try:
                data_json = fetch_stock_data(ticker, "5d")
                data = json.loads(data_json)

                tech_json = calculate_technical_indicators(ticker, "3mo")
                tech = json.loads(tech_json)

                # Check for alerts
                ticker_alerts = []

                if tech['signals']['rsi_overbought']:
                    ticker_alerts.append("RSI Overbought (>70)")
                if tech['signals']['rsi_oversold']:
                    ticker_alerts.append("RSI Oversold (<30)")
                if tech['signals']['macd_bullish_crossover']:
                    ticker_alerts.append("MACD Bullish Crossover")
                if tech['signals']['golden_cross']:
                    ticker_alerts.append("Golden Cross (Bullish)")
                if tech['signals']['death_cross']:
                    ticker_alerts.append("Death Cross (Bearish)")

                if ticker_alerts:
                    alerts.append(f"**{ticker}:** {', '.join(ticker_alerts)}")

                portfolio_data.append({
                    'Ticker': ticker,
                    'Price': data['current_price'],
                    'Change %': data['change_percent'],
                    'RSI': tech['indicators']['RSI'],
                    'Trend': tech['overall_trend'],
                    'Alerts': len(ticker_alerts)
                })

            except Exception as e:
                log.error(f"Error monitoring {ticker}: {str(e)}")
                continue

        # Create summary
        df = pd.DataFrame(portfolio_data)

        summary = f"""
## Portfolio Monitor
**Last Updated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

### Holdings Summary:
{df.to_markdown(index=False)}

### Alerts:
"""
        if alerts:
            summary += "\n".join([f"- {alert}" for alert in alerts])
        else:
            summary += "No alerts at this time."

        # Create portfolio composition chart
        fig = go.Figure()

        # Bar chart of change percentages
        colors = ['green' if x >= 0 else 'red' for x in df['Change %']]

        fig.add_trace(
            go.Bar(
                x=df['Ticker'],
                y=df['Change %'],
                marker_color=colors,
                text=df['Change %'].apply(lambda x: f"{x:+.2f}%"),
                textposition='outside'
            )
        )

        fig.update_layout(
            title='Portfolio Performance (Today)',
            yaxis_title='Change (%)',
            xaxis_title='Stock',
            height=400,
            template='plotly_dark',
            showlegend=False
        )

        return summary, fig

    except Exception as e:
        error_msg = f"Error monitoring portfolio: {str(e)}"
        log.error(error_msg)
        return error_msg, None


# Create Gradio UI
def create_ui():
    """Create and configure the Gradio interface."""

    with gr.Blocks(title="Financial Agent", theme=gr.themes.Soft()) as app:

        gr.Markdown("""
        # Financial Agent
        ### AI-Powered Stock Market Analysis

        Analyze stocks, compare performance, and monitor your portfolio using natural language and interactive dashboards.
        """)

        with gr.Tabs():

            # Tab 1: Chat Interface
            with gr.Tab("Chat Assistant"):
                gr.Markdown("""
                ### Ask me anything about stocks!

                **Example questions:**
                - "What is the current price of Apple?"
                - "Should I buy Tesla stock?"
                - "Compare Amazon and Microsoft"
                - "Is NVIDIA overbought?"
                """)

                chatbot = gr.Chatbot(height=500)
                msg = gr.Textbox(
                    label="Your Question",
                    placeholder="Ask about any stock...",
                    lines=2
                )

                with gr.Row():
                    submit = gr.Button("Send", variant="primary")
                    clear = gr.Button("Clear Chat")

                # Chat examples
                gr.Examples(
                    examples=[
                        "What is the current price of Apple (AAPL)?",
                        "Is Tesla oversold based on RSI?",
                        "Compare AAPL and MSFT technical indicators",
                        "Should I buy NVIDIA stock right now?",
                        "What are the support levels for Amazon?",
                    ],
                    inputs=msg
                )

                # Chat functionality
                def respond(message, chat_history):
                    bot_response = chat_with_agent(message, chat_history)
                    chat_history.append((message, bot_response))
                    return "", chat_history

                msg.submit(respond, [msg, chatbot], [msg, chatbot])
                submit.click(respond, [msg, chatbot], [msg, chatbot])
                clear.click(lambda: None, None, chatbot, queue=False)

            # Tab 2: Stock Dashboard
            with gr.Tab("Stock Dashboard"):
                gr.Markdown("### Comprehensive Stock Analysis with Interactive Charts")

                with gr.Row():
                    ticker_input = gr.Textbox(
                        label="Stock Ticker",
                        placeholder="Enter ticker (e.g., AAPL)",
                        value="AAPL"
                    )
                    period_input = gr.Dropdown(
                        choices=["1mo", "3mo", "6mo", "1y", "2y"],
                        value="3mo",
                        label="Time Period"
                    )
                    analyze_btn = gr.Button("Analyze", variant="primary")

                with gr.Row():
                    summary_output = gr.Markdown()

                with gr.Row():
                    price_chart_output = gr.Plot(label="Price Chart")

                with gr.Row():
                    indicators_chart_output = gr.Plot(label="Technical Indicators")

                with gr.Row():
                    tech_details_output = gr.Markdown()

                analyze_btn.click(
                    fn=analyze_stock,
                    inputs=[ticker_input, period_input],
                    outputs=[summary_output, price_chart_output, indicators_chart_output, tech_details_output]
                )

            # Tab 3: Stock Comparison
            with gr.Tab("Compare Stocks"):
                gr.Markdown("### Side-by-Side Stock Comparison")

                with gr.Row():
                    compare_input = gr.Textbox(
                        label="Stock Tickers (comma-separated)",
                        placeholder="e.g., AAPL, MSFT, GOOGL",
                        value="AAPL, MSFT, GOOGL"
                    )
                    compare_btn = gr.Button("Compare", variant="primary")

                with gr.Row():
                    compare_text_output = gr.Markdown()

                with gr.Row():
                    compare_chart_output = gr.Plot(label="Performance Comparison")

                compare_btn.click(
                    fn=compare_stocks,
                    inputs=[compare_input],
                    outputs=[compare_text_output, compare_chart_output]
                )

            # Tab 4: Portfolio Monitor
            with gr.Tab("Portfolio Monitor"):
                gr.Markdown("### Monitor Your Portfolio and Get Alerts")

                with gr.Row():
                    portfolio_input = gr.Textbox(
                        label="Portfolio Tickers (comma-separated)",
                        placeholder="e.g., AAPL, TSLA, NVDA",
                        value="AAPL, TSLA, NVDA"
                    )
                    monitor_btn = gr.Button("Monitor", variant="primary")
                    refresh_btn = gr.Button("Refresh", variant="secondary")

                with gr.Row():
                    portfolio_summary_output = gr.Markdown()

                with gr.Row():
                    portfolio_chart_output = gr.Plot(label="Portfolio Performance")

                monitor_btn.click(
                    fn=monitor_portfolio,
                    inputs=[portfolio_input],
                    outputs=[portfolio_summary_output, portfolio_chart_output]
                )

                refresh_btn.click(
                    fn=monitor_portfolio,
                    inputs=[portfolio_input],
                    outputs=[portfolio_summary_output, portfolio_chart_output]
                )

        gr.Markdown("""
        ---
        **Note:** Data is provided by Yahoo Finance (15-minute delay). This is for educational purposes only and not financial advice.
        """)

    return app


if __name__ == "__main__":
    log.info("Starting Financial Agent UI...")
    ui = create_ui()
    ui.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        show_error=True
    )
