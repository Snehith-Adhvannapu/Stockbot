


<p align="center">
  <strong>🚀 Algora - AI Stock Trading Platform</strong><br/>
  <em>AI-Powered Trading Made Simple</em>
</p>

---

## 📖 Project Description
✨ **Problem Statement:** Retail investors struggle to make informed trading decisions due to lack of access to sophisticated analysis tools, real-time market insights, and automated trading capabilities that were previously only available to institutional investors.

💡 **Proposed Solution:** Algora is a comprehensive AI-powered stock trading platform that combines multi-agent AI analysis, autonomous trading bots, real-time market monitoring, and portfolio management. The platform uses advanced sentiment analysis, fundamental research, and technical indicators to provide actionable trading insights in INR for the Indian market.

🎯 **Target Users / Use Cases:** 
- Retail investors seeking AI-powered stock recommendations
- Traders wanting to automate their trading strategies with paper trading
- Portfolio managers needing real-time analytics and risk management
- Market enthusiasts looking for pattern recognition and technical analysis tools

---

## 🔬 Methodology
1. **Research & Ideation** – Analyzed pain points of retail investors and identified need for accessible AI trading tools
2. **Design** – Created multi-agent architecture with Streamlit UI, designed autonomous trading bot system
3. **Develop** – Implemented core features:
   - AI Stock Advisor with sentiment & fundamental analysis
   - Autonomous Trading Bot with customizable strategies
   - Real-time Portfolio Manager with INR conversion
   - Market Scanner with pattern recognition
   - Interactive Dashboard with live metrics
4. **Test** – Paper trading mode for risk-free testing, backtesting engine for strategy validation
5. **Deploy** – Streamlit deployment on Replit with Alpaca API integration
6. **Future Scope** – Live trading mode, options trading, ML-based strategy optimization, mobile app

---



---

## 🛠️ Technology Stack
`Python` | `Streamlit` | `Alpaca Trading API` | `yfinance` | `NewsAPI` | `NLTK` | `spaCy` | `Plotly` | `Pandas` | `NumPy` | `Beautiful Soup`

**Key Libraries:**
- **Frontend**: Streamlit for interactive web UI
- **AI/NLP**: NLTK & spaCy for sentiment analysis
- **Trading**: Alpaca-py for paper/live trading
- **Data**: yfinance for market data, NewsAPI for news
- **Visualization**: Plotly for interactive charts
- **Analysis**: Pandas & NumPy for data processing

---

## 📹 Demonstration Video
▶️ https://drive.google.com/file/d/1CXYzeex3RMo6V6vJFmSxa9k1VdFblIhj/view?usp=sharing

---

## 🌐 Deployment
🔗 [Live Demo Link](#)

---

## 📚 References
- [Alpaca Trading API Documentation](https://alpaca.markets/docs/)
- [yfinance Library](https://pypi.org/project/yfinance/)
- [NewsAPI](https://newsapi.org/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [spaCy NLP](https://spacy.io/)

---

## 🖼️ Assets / Screenshots
<p align="center">
  <img src="assets/dashboard_screenshot.png" alt="Trading Dashboard" width="600" /><br/>
  <em>Real-time Trading Dashboard with Live Metrics</em>
</p>

<p align="center">
  <img src="assets/ai_advisor_screenshot.png" alt="AI Stock Advisor" width="600" /><br/>
  <em>AI-Powered Stock Analysis & Recommendations</em>
</p>

<p align="center">
  <img src="assets/trading_bot_screenshot.png" alt="Autonomous Trading Bot" width="600" /><br/>
  <em>Autonomous Trading Bot Configuration</em>
</p>

---

## ✨ Key Features

### 🧠 AI Stock Advisor
- Multi-agent analysis system (Fundamental + Sentiment)
- Real-time news sentiment analysis
- Financial metrics evaluation (PE, ROE, PB ratios)
- BUY/HOLD/SELL recommendations
- Sector-based stock screening

### 🤖 Autonomous Trading Bot
- Customizable trading strategies (Momentum, Mean Reversion, Breakout)
- Paper trading mode for risk-free testing
- Automated buy/sell execution
- Real-time performance tracking
- Stop-loss and take-profit automation

### 📊 Portfolio Manager
- Real-time portfolio tracking
- USD to INR conversion
- Position analysis with P/L metrics
- Risk management insights
- Performance analytics

### 📈 Market Tools
- Live market scanner with top gainers/losers
- Pattern recognition (Head & Shoulders, Double Top/Bottom)
- Technical indicator analysis (RSI, MACD, Bollinger Bands)
- Customizable watchlists
- Interactive charting

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- NewsAPI key (free at [newsapi.org](https://newsapi.org))

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/ai-stock-advisor.git
   cd ai-stock-advisor
   ```

2. **Install dependencies**
   ```bash
   pip install streamlit pandas numpy yfinance requests beautifulsoup4 trafilatura nltk spacy plotly python-dateutil
   python -m spacy download en_core_web_sm
   ```

3. **Set up environment variables**
   ```bash
   export NEWS_API_KEY="your_newsapi_key_here"
   ```

4. **Run the application**
   ```bash
   streamlit run app.py --server.port 5000
   ```

5. **Open your browser** to `http://localhost:5000`

## 🏗️ Architecture

### Multi-Agent System

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ Screening Agent │    │Fundamental Agent│    │ Sentiment Agent │
│                 │    │                 │    │                 │
│ • Sector stocks │    │ • yfinance API  │    │ • NewsAPI       │
│ • Stock lists   │    │ • PE, PB, ROE   │    │ • NLTK VADER    │
│ • Fallback data │    │ • Market cap    │    │ • spaCy NLP     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────┐
                    │ Aggregator Agent│
                    │                 │
                    │ • Score fusion  │
                    │ • Recommendations│
                    │ • BUY/HOLD/SELL │
                    └─────────────────┘
```

### Key Components

- **🎯 Screening Agent**: Curated stock lists by sector with fallback mechanisms
- **📊 Fundamental Agent**: Financial analysis using yfinance (PE, PB, ROE, etc.)
- **📰 Sentiment Agent**: News sentiment analysis using NewsAPI + NLP
- **🔧 Aggregator Agent**: Weighted score combination and final recommendations
- **💾 Cache Manager**: Two-tier caching (memory + file) for performance
- **📏 Data Normalizer**: Standardized 0-100 scoring across all metrics

## 📋 Usage Guide

### 1. Choose Your Sector
Select from predefined sectors:
- 🖥️ **IT & Tech**: TCS, INFY, HCLTECH, WIPRO, TECHM
- 🏦 **Banking**: HDFCBANK, ICICIBANK, SBI, KOTAKBANK, AXISBANK
- 🚗 **Auto**: MARUTI, TATAMOTORS, M&M, BAJAJ-AUTO, EICHERMOT
- ⚗️ **Pharma**: SUNPHARMA, DRREDDY, CIPLA, DIVISLAB, BIOCON
- 🌿 **Green Energy**: ADANIGREEN, SUZLON, TATAPOWER, NTPC, POWERGRID
- 🏭 **Diversified**: RELIANCE, ITC, HINDUNILVR, LT, ASIANPAINT

### 2. Set Analysis Balance
Use the interactive slider to adjust weighting:
- **Left (0%)**: Pure fundamental analysis
- **Center (50%)**: Balanced approach
- **Right (100%)**: Pure sentiment analysis

### 3. Advanced Options
- **Stock Count**: Analyze 3-10 stocks per sector
- **Risk Tolerance**: Conservative, Moderate, or Aggressive

### 4. Review Results
- **Summary Cards**: Quick overview of BUY/HOLD/SELL counts
- **Performance Chart**: Visual comparison of all analyzed stocks
- **Detailed Cards**: Expandable analysis with full metrics and reasoning

## 🔧 Configuration

### Environment Variables
```bash
NEWS_API_KEY=your_newsapi_key_here
```

### Streamlit Configuration
Create `.streamlit/config.toml`:
```toml
[server]
headless = true
address = "0.0.0.0"
port = 5000

[theme]
primaryColor = "#667eea"
backgroundColor = "#0e1117"
secondaryBackgroundColor = "#262730"
textColor = "#fafafa"
```

## 📊 API Reference

### External APIs Used

1. **yfinance**: Stock fundamental data (no authentication required)
   - Financial ratios (PE, PB, ROE)
   - Market cap and pricing data
   - Company information

2. **NewsAPI**: Latest news headlines (requires free API key)
   - Company-specific news search
   - Real-time market sentiment
   - Article content analysis

3. **NLTK**: Natural language processing
   - VADER sentiment analyzer
   - Text preprocessing and tokenization

4. **spaCy**: Advanced NLP pipeline
   - Named entity recognition
   - Advanced text analysis

## 🎯 Scoring System

### Fundamental Scoring (0-100)
- **PE Ratio**: Optimized for Indian market (15-25 range)
- **PB Ratio**: Book value assessment (1-3 range)
- **ROE**: Return on equity evaluation (>15% preferred)
- **Debt-to-Equity**: Financial stability (lower is better)
- **Profit Margins**: Operational efficiency

### Sentiment Scoring (0-100)
- **Article Coverage**: Number of recent news articles
- **Sentiment Ratio**: Positive vs negative news balance
- **Volatility**: Consistency of sentiment over time
- **Entity Recognition**: Company mention frequency

### Final Recommendations
- **BUY**: Score ≥ 70
- **HOLD**: Score 50-69
- **SELL**: Score < 50

## 🚧 Development

### Project Structure
```
ai-stock-advisor/
├── agents/
│   ├── screening_agent.py      # Stock discovery and selection
│   ├── fundamental_agent.py    # Financial analysis
│   ├── sentiment_agent.py      # News sentiment analysis
│   └── aggregator_agent.py     # Score aggregation
├── utils/
│   ├── cache_manager.py        # Caching system
│   └── data_normalizer.py      # Score normalization
├── .streamlit/
│   └── config.toml            # Streamlit configuration
├── app.py                     # Main application
├── requirements.txt           # Python dependencies
├── README.md                 # This file
└── replit.md                 # Project documentation
```

### Adding New Sectors
1. Update sector dictionary in `app.py`
2. Add corresponding stock tickers
3. Test with your desired stock count

### Customizing Scoring
1. Modify `DataNormalizer` class for different score ranges
2. Adjust recommendation thresholds in `AggregatorAgent`
3. Update sector-specific benchmarks

## 🔒 Security & Limitations

### Security Considerations
- API keys are handled via environment variables
- No financial advice disclaimer required
- Rate limiting implemented for external APIs
- Input validation for all user parameters

### Current Limitations
- **Demo Purpose**: Built for hackathons, not production trading
- **Indian Market Focus**: Optimized for NSE-listed stocks
- **API Dependencies**: Requires stable internet and valid API keys
- **No Real-time Trading**: Analysis only, no order execution
- **Cache TTL**: 1-hour cache may not reflect rapid market changes


<p align="center">
  <b>Hackathon:</b> AIGNITE 2K25 | Organized by MLSC<br/>
  <b>Built with ❤️ using AI and Open Source Technologies</b>
</p>


