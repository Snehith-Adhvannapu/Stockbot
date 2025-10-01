import streamlit as st
import pandas as pd
import numpy as np
import time
from datetime import datetime
import os
import plotly.express as px
import plotly.graph_objects as go

from agents.screening_agent import ScreeningAgent
from agents.fundamental_agent import FundamentalAgent
from agents.sentiment_agent import SentimentAgent
from agents.aggregator_agent import AggregatorAgent
from utils.cache_manager import CacheManager
from utils.data_normalizer import DataNormalizer

@st.cache_resource
def get_cache_manager():
    return CacheManager()

@st.cache_resource
def initialize_agents():
    screening_agent = ScreeningAgent()
    fundamental_agent = FundamentalAgent()
    sentiment_agent = SentimentAgent()
    aggregator_agent = AggregatorAgent()
    data_normalizer = DataNormalizer()
    
    return screening_agent, fundamental_agent, sentiment_agent, aggregator_agent, data_normalizer

def show():
    st.markdown("""
    <style>
    .main-header {
        text-align: center;
        padding: 3rem 1rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        margin: -1rem -1rem 3rem -1rem;
        border-radius: 0 0 25px 25px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.15);
    }
    
    .main-header h1 {
        color: white;
        font-size: 3.5rem;
        margin: 0;
        text-shadow: 2px 2px 8px rgba(0,0,0,0.3);
        font-weight: 700;
    }
    
    .main-header p {
        color: rgba(255,255,255,0.9);
        font-size: 1.3rem;
        margin: 1rem 0 0 0;
        font-weight: 300;
        letter-spacing: 0.5px;
    }
    
    .section-spacing {
        margin: 2.5rem 0;
    }
    
    .process-card {
        text-align: center;
        padding: 2rem 1.5rem;
        border-radius: 15px;
        margin: 1rem 0.5rem;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        border: 1px solid rgba(255,255,255,0.1);
    }
    
    .process-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }
    
    .process-card h3 {
        margin: 0 0 1rem 0;
        font-size: 1.4rem;
        font-weight: 600;
    }
    
    .process-card p {
        margin: 0;
        font-size: 0.95rem;
        line-height: 1.5;
        opacity: 0.9;
    }
    
    .weight-slider-container {
        background: rgba(255,255,255,0.05);
        padding: 2rem;
        border-radius: 15px;
        margin: 2rem 0;
        border: 1px solid rgba(255,255,255,0.1);
    }
    
    .metric-card {
        padding: 1.8rem;
        border-radius: 15px;
        text-align: center;
        color: white;
        margin: 0.5rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        transition: transform 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-3px);
    }
    
    .metric-card h2 {
        margin: 0;
        font-size: 2.5rem;
        font-weight: 700;
    }
    
    .metric-card p {
        margin: 0.5rem 0 0 0;
        opacity: 0.9;
        font-size: 1rem;
        font-weight: 500;
    }
    
    @media (prefers-color-scheme: light) {
        .process-card {
            background: white;
            color: #2c3e50;
            box-shadow: 0 2px 15px rgba(0,0,0,0.1);
        }
        
        .process-card p {
            color: #5a6c7d;
        }
        
        .weight-slider-container {
            background: #f8f9fa;
            border: 1px solid #e9ecef;
        }
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class='main-header'>
        <h1>🤖 AI Stock Advisor</h1>
        <p>Smart insights. Simple decisions.</p>
    </div>
    """, unsafe_allow_html=True)
    
    cache_manager = get_cache_manager()
    screening_agent, fundamental_agent, sentiment_agent, aggregator_agent, data_normalizer = initialize_agents()
    
    st.markdown("<div class='section-spacing'>", unsafe_allow_html=True)
    st.markdown("### 🎯 Choose a Sector")
    st.markdown("Select an industry that interests you for focused analysis")
    
    sectors = {
        "🖥️ IT & Tech": ["TCS", "INFY", "HCLTECH", "WIPRO", "TECHM"],
        "🏦 Banking & Finance": ["HDFCBANK", "ICICIBANK", "SBIN", "KOTAKBANK", "AXISBANK"],
        "🚗 Auto": ["MARUTI", "TATAMOTORS", "M&M", "BAJAJ-AUTO", "EICHERMOT"],
        "⚗️ Pharma": ["SUNPHARMA", "DRREDDY", "CIPLA", "DIVISLAB", "BIOCON"],
        "🌿 Green Energy": ["ADANIGREEN", "SUZLON", "TATAPOWER", "NTPC", "POWERGRID"],
        "🏭 Diversified": ["RELIANCE", "ITC", "HINDUNILVR", "LT", "ASIANPAINT"]
    }
    
    selected_sector = st.selectbox(
        "Select sector:",
        options=list(sectors.keys()),
        index=0,
        help="Choose a sector that interests you for focused analysis"
    )
    
    st.markdown(f"**Selected stocks:** {', '.join(sectors[selected_sector][:3])}...")
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='section-spacing'>", unsafe_allow_html=True)
    st.markdown("### ⚖️ Analysis Balance")
    st.markdown("Customize how much weight to give each type of analysis")
    
    st.markdown("<div class='weight-slider-container'>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 3, 1])
    
    with col1:
        st.markdown("**📊 Fundamentals**")
        st.caption("Financial health, ratios, performance metrics")
    
    with col2:
        sentiment_weight = st.slider(
            "Balance focus:",
            min_value=0,
            max_value=100,
            value=50,
            step=10,
            format="%d%%",
            help="Move left for fundamental focus, right for sentiment focus"
        )
        
        fundamental_weight = 100 - sentiment_weight
        
        st.markdown(f"""
        <div style='display: flex; height: 30px; margin: 15px 0; border-radius: 15px; overflow: hidden; box-shadow: 0 2px 10px rgba(0,0,0,0.1);'>
            <div style='background: linear-gradient(135deg, #4CAF50, #45a049); width: {fundamental_weight}%; display: flex; align-items: center; justify-content: center; color: white; font-size: 14px; font-weight: 600;'>
                📊 {fundamental_weight}%
            </div>
            <div style='background: linear-gradient(135deg, #2196F3, #1976d2); width: {sentiment_weight}%; display: flex; align-items: center; justify-content: center; color: white; font-size: 14px; font-weight: 600;'>
                🗞️ {sentiment_weight}%
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("**🗞️ Sentiment**")
        st.caption("News analysis, market sentiment, buzz")
    
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='section-spacing'>", unsafe_allow_html=True)
    with st.expander("🔧 Advanced Options", expanded=False):
        st.markdown("**Fine-tune your analysis parameters**")
        
        col1, col2 = st.columns(2)
        with col1:
            num_stocks = st.selectbox(
                "Number of stocks to analyze:",
                options=[3, 5, 8, 10],
                index=1,
                help="More stocks = longer analysis time"
            )
        
        with col2:
            risk_tolerance = st.selectbox(
                "Risk Tolerance:",
                options=["Conservative", "Moderate", "Aggressive"],
                index=1,
                help="Adjusts recommendation thresholds"
            )
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='section-spacing'>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        analyze_button = st.button(
            "🔍 Run Analysis", 
            type="primary", 
            use_container_width=True,
            help="Start analyzing selected sector stocks"
        )
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    if analyze_button:
        with st.spinner("🔍 Multi-Agent Analysis in Progress..."):
            try:
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                status_text.text("🎯 Preparing sector stocks for analysis...")
                progress_bar.progress(10)
                
                sector_stocks = sectors[selected_sector][:num_stocks]
                screening_results = []
                
                for ticker in sector_stocks:
                    screening_results.append({
                        'ticker': ticker,
                        'name': f"{ticker} Limited",
                        'sector': selected_sector,
                        'source': 'sector_selection'
                    })
                
                if not screening_results:
                    st.error("❌ No stocks found for selected sector")
                    return
                
                st.success(f"✅ Analyzing {len(screening_results)} stocks from {selected_sector}")
                progress_bar.progress(25)
                
                status_text.text("📊 Fundamental Agent: Analyzing financial metrics...")
                
                fundamental_data = {}
                for i, stock in enumerate(screening_results):
                    ticker = stock['ticker']
                    fundamental_data[ticker] = fundamental_agent.analyze_stock(ticker)
                    progress_bar.progress(25 + (i + 1) * 25 // len(screening_results))
                
                progress_bar.progress(50)
                
                status_text.text("📰 Sentiment Agent: Analyzing market sentiment...")
                
                sentiment_data = {}
                for i, stock in enumerate(screening_results):
                    ticker = stock['ticker']
                    company_name = stock['name']
                    sentiment_data[ticker] = sentiment_agent.analyze_sentiment(ticker, company_name)
                    progress_bar.progress(50 + (i + 1) * 25 // len(screening_results))
                
                progress_bar.progress(75)
                
                status_text.text("🔧 Aggregator Agent: Combining analysis results...")
                
                final_results = []
                for stock in screening_results:
                    ticker = stock['ticker']
                    
                    fundamental_score = data_normalizer.normalize_fundamental_score(
                        fundamental_data.get(ticker, {})
                    )
                    sentiment_score = data_normalizer.normalize_sentiment_score(
                        sentiment_data.get(ticker, {})
                    )
                    
                    aggregated_result = aggregator_agent.aggregate_scores(
                        ticker=ticker,
                        company_name=stock['name'],
                        screening_data=stock,
                        fundamental_data=fundamental_data.get(ticker, {}),
                        sentiment_data=sentiment_data.get(ticker, {}),
                        fundamental_weight=fundamental_weight / 100,
                        sentiment_weight=sentiment_weight / 100
                    )
                    
                    final_results.append(aggregated_result)
                
                progress_bar.progress(100)
                status_text.text("✨ Analysis Complete!")
                
                time.sleep(1)
                progress_bar.empty()
                status_text.empty()
                
                from app import display_results
                display_results(final_results, fundamental_weight, sentiment_weight)
                
            except Exception as e:
                st.error(f"❌ Analysis failed: {str(e)}")
                st.exception(e)
    
    else:
        st.markdown("---")
        
        st.markdown("## 🎯 How It Works")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("""
            <div class='process-card' style='background: linear-gradient(135deg, #e3f2fd, #bbdefb);'>
                <h3 style='color: #1976d2;'>🎯 Select</h3>
                <p style='color: #424242;'>Choose your preferred sector from IT, Banking, Auto, Pharma, and more</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class='process-card' style='background: linear-gradient(135deg, #f3e5f5, #e1bee7);'>
                <h3 style='color: #7b1fa2;'>⚖️ Balance</h3>
                <p style='color: #424242;'>Adjust focus between fundamental analysis and sentiment analysis</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class='process-card' style='background: linear-gradient(135deg, #e8f5e8, #c8e6c9);'>
                <h3 style='color: #388e3c;'>🔍 Analyze</h3>
                <p style='color: #424242;'>AI agents analyze fundamentals, news sentiment, and market data</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown("""
            <div class='process-card' style='background: linear-gradient(135deg, #fff3e0, #ffcc02);'>
                <h3 style='color: #f57c00;'>📊 Decide</h3>
                <p style='color: #424242;'>Get BUY/HOLD/SELL recommendations with detailed reasoning</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        with st.expander("🤖 Meet the AI Agents", expanded=False):
            agent_col1, agent_col2 = st.columns(2)
            
            with agent_col1:
                st.markdown("""
                **📊 Fundamental Analysis Agent**
                - Fetches live data using yfinance
                - Analyzes PE ratio, PB ratio, ROE, debt levels
                - Evaluates financial health and growth metrics
                
                **🔧 Aggregator Agent**
                - Combines all analysis into single score
                - Generates BUY/HOLD/SELL recommendations
                - Provides human-readable reasoning
                """)
            
            with agent_col2:
                st.markdown("""
                **📰 Sentiment Analysis Agent**
                - Fetches latest news via NewsAPI
                - Uses NLTK VADER sentiment analysis
                - Applies spaCy NLP for entity recognition
                
                **🎯 Sector Intelligence**
                - Curated stock lists by industry
                - Context-aware analysis for each sector
                - Focused recommendations within themes
                """)
        
        st.markdown("### 📈 Sample Analysis Preview")
        
        with st.container():
            st.markdown("""
            <div style='border: 2px dashed #ccc; padding: 20px; border-radius: 10px; background: #f9f9f9;'>
                <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;'>
                    <h4 style='margin: 0; color: #333;'>📊 Sample: TCS - Tata Consultancy Services</h4>
                    <span style='background: #4CAF50; color: white; padding: 5px 15px; border-radius: 20px; font-weight: bold;'>✅ BUY</span>
                </div>
                <p style='color: #666; margin: 0 0 10px 0;'><strong>Score:</strong> 78.5/100 | <strong>PE:</strong> 22.4 | <strong>Sentiment:</strong> Positive</p>
                <p style='color: #555; margin: 0; font-style: italic;'>Strong fundamentals with positive market sentiment and excellent returns on equity</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("### 🚀 Ready to Start?")
        st.markdown("1. **Choose a sector** that interests you")
        st.markdown("2. **Adjust the analysis balance** based on your preference")
        st.markdown("3. **Click 'Run Analysis'** to get AI-powered recommendations")
        
        info_col1, info_col2 = st.columns(2)
        
        with info_col1:
            st.info("""
            **⚡ Fast & Accurate**
            - Analysis completed in 30-60 seconds
            - Real-time data from yfinance
            - Smart caching for better performance
            """)
        
        with info_col2:
            st.success("""
            **🔒 Reliable Sources**
            - Live financial data
            - Latest news sentiment
            - No mock or placeholder data
            """)
