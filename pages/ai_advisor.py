import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import time
from datetime import datetime

from agents.screening_agent import ScreeningAgent
from agents.fundamental_agent import FundamentalAgent
from agents.sentiment_agent import SentimentAgent
from agents.aggregator_agent import AggregatorAgent
from utils.cache_manager import CacheManager
from utils.data_normalizer import DataNormalizer

SECTORS = {
    "🖥️ IT & Tech (India)": ["TCS", "INFY", "HCLTECH", "WIPRO", "TECHM"],
    "🖥️ IT & Tech (US)": ["AAPL", "MSFT", "GOOGL", "META", "NVDA"],
    "🏦 Banking (India)": ["HDFCBANK", "ICICIBANK", "SBI", "KOTAKBANK", "AXISBANK"],
    "🏦 Banking (US)": ["JPM", "BAC", "WFC", "C", "GS"],
    "🚗 Auto (India)": ["MARUTI", "TATAMOTORS", "M&M", "BAJAJ-AUTO", "EICHERMOT"],
    "🚗 Auto (US)": ["TSLA", "F", "GM", "RIVN", "LCID"],
    "⚗️ Pharma (India)": ["SUNPHARMA", "DRREDDY", "CIPLA", "DIVISLAB", "BIOCON"],
    "⚗️ Pharma (US)": ["PFE", "JNJ", "ABBV", "MRK", "LLY"],
    "🌿 Green Energy (India)": ["ADANIGREEN", "SUZLON", "TATAPOWER", "NTPC", "POWERGRID"],
    "🌿 Green Energy (US)": ["ENPH", "SEDG", "NEE", "FSLR", "RUN"],
    "🏭 Diversified (India)": ["RELIANCE", "ITC", "HINDUNILVR", "LT", "ASIANPAINT"],
    "🏭 Diversified (US)": ["BRK.B", "JNJ", "PG", "KO", "PEP"]
}

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
    st.title("🧠 AI Stock Advisor")
    st.markdown("Intelligent stock recommendations powered by AI sentiment analysis and fundamental research")
    
    st.markdown("---")
    
    st.markdown("### 1. Select Analysis Mode")
    analysis_type = st.radio(
        "Choose your analysis approach:",
        ["📊 Sector Analysis", "✏️ Custom Stocks"],
        horizontal=True,
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    if analysis_type == "📊 Sector Analysis":
        st.markdown("### 2. Choose Your Sector")
        st.markdown("Select from predefined sectors:")
        
        selected_sector = st.selectbox(
            "Sector",
            options=list(SECTORS.keys()),
            label_visibility="collapsed",
            key="sector_select"
        )
        
        sector_stocks = SECTORS[selected_sector]
        st.caption(f"**Stocks:** {', '.join(sector_stocks)}")
        
        stocks_to_use = sector_stocks
        analysis_mode = 'sector'
        display_name = selected_sector
    else:
        st.markdown("### 2. Enter Your Stocks")
        st.markdown("Enter the stock symbols you want to analyze:")
        
        custom_input = st.text_area(
            "Enter symbols (one per line):",
            value="",
            height=150,
            placeholder="AAPL\nMSFT\nGOOGL\nTSLA\nNVDA",
            key="custom_stocks_input"
        )
        
        custom_stocks = [s.strip().upper() for s in custom_input.split('\n') if s.strip()]
        if custom_stocks:
            st.caption(f"✓ Ready to analyze {len(custom_stocks)} stocks")
        else:
            st.caption("⚠️ Please enter at least one stock symbol")
        
        stocks_to_use = custom_stocks
        analysis_mode = 'custom'
        display_name = "Custom Stocks"
    
    st.markdown("---")
    
    st.markdown("### 3. Set Analysis Balance")
    st.markdown("Use the interactive slider to adjust weighting:")
    
    balance = st.slider(
        "Analysis Balance",
        min_value=0,
        max_value=100,
        value=50,
        help="Left (0%): Pure fundamental analysis | Center (50%): Balanced approach | Right (100%): Pure sentiment analysis",
        label_visibility="collapsed"
    )
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.caption("**Left (0%):** Pure fundamental analysis")
    with col2:
        st.caption("**Center (50%):** Balanced approach")
    with col3:
        st.caption("**Right (100%):** Pure sentiment analysis")
    
    fundamental_weight = (100 - balance) / 100
    sentiment_weight = balance / 100
    
    st.markdown("---")
    
    st.markdown("### 4. Advanced Options")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if analysis_mode == "sector":
            stock_count = st.slider(
                "Stock Count",
                min_value=3,
                max_value=min(10, len(stocks_to_use)),
                value=min(5, len(stocks_to_use)),
                help="Analyze 3-10 stocks per sector"
            )
            st.caption("Number of stocks to analyze from sector")
        else:
            stock_count = len(stocks_to_use)
            st.info(f"Will analyze all {stock_count} custom stocks")
    
    with col2:
        risk_tolerance = st.select_slider(
            "Risk Tolerance",
            options=["Conservative", "Moderate", "Aggressive"],
            value="Moderate"
        )
        st.caption("Select your risk profile")
    
    st.markdown("---")
    
    button_label = "🔍 Analyze Sector" if analysis_mode == "sector" else "🔍 Analyze Stocks"
    analyze_button = st.button(button_label, type="primary", use_container_width=True, disabled=(analysis_mode == "custom" and len(stocks_to_use) == 0))
    
    if analyze_button:
        if analysis_mode == "sector":
            stocks_to_analyze = stocks_to_use[:stock_count]
        else:
            stocks_to_analyze = stocks_to_use
        
        with st.spinner(f"Analyzing {len(stocks_to_analyze)} stocks from {display_name}..."):
            try:
                screening_agent, fundamental_agent, sentiment_agent, aggregator_agent, data_normalizer = initialize_agents()
                cache_manager = get_cache_manager()
                
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                all_results = []
                
                for idx, stock in enumerate(stocks_to_analyze):
                    if analysis_mode == "sector" and "(India)" in display_name:
                        symbol = f"{stock}.NS"
                    else:
                        symbol = stock
                    
                    status_text.text(f"Analyzing {stock} ({idx + 1}/{len(stocks_to_analyze)})...")
                    
                    try:
                        sentiment_result = sentiment_agent.analyze_sentiment(symbol, stock)
                        fundamental_result = fundamental_agent.analyze_stock(symbol)
                        
                        final_recommendation = aggregator_agent.aggregate_scores(
                            ticker=symbol,
                            company_name=stock,
                            screening_data={},
                            fundamental_data=fundamental_result,
                            sentiment_data=sentiment_result,
                            fundamental_weight=fundamental_weight,
                            sentiment_weight=sentiment_weight
                        )
                        
                        analysis_results = {
                            'symbol': stock,
                            'sentiment': sentiment_result,
                            'fundamental': fundamental_result,
                            'weights': {
                                'sentiment': sentiment_weight,
                                'fundamental': fundamental_weight
                            }
                        }
                        
                        all_results.append({
                            'stock': stock,
                            'analysis': analysis_results,
                            'recommendation': final_recommendation
                        })
                        
                    except Exception as e:
                        st.warning(f"Could not analyze {stock}: {str(e)}")
                    
                    progress_bar.progress((idx + 1) / len(stocks_to_analyze))
                
                status_text.text("✅ Analysis complete!")
                time.sleep(0.5)
                progress_bar.empty()
                status_text.empty()
                
                st.session_state.analysis_results = all_results
                st.session_state.sector = display_name
                st.session_state.risk_tolerance = risk_tolerance
                
            except Exception as e:
                st.error(f"Analysis failed: {str(e)}")
                return
    
    if 'analysis_results' in st.session_state and st.session_state.analysis_results:
        results = st.session_state.analysis_results
        
        st.markdown("---")
        st.markdown("### 5. Review Results")
        
        st.markdown("#### Summary Cards")
        st.markdown("Quick overview of BUY/HOLD/SELL counts")
        
        buy_count = sum(1 for r in results if r['recommendation'].get('recommendation') == 'BUY')
        hold_count = sum(1 for r in results if r['recommendation'].get('recommendation') == 'HOLD')
        sell_count = sum(1 for r in results if r['recommendation'].get('recommendation') == 'SELL')
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("🟢 BUY", buy_count)
        with col2:
            st.metric("🟡 HOLD", hold_count)
        with col3:
            st.metric("🔴 SELL", sell_count)
        
        st.markdown("#### Performance Chart")
        st.markdown("Visual comparison of all analyzed stocks")
        
        chart_data = []
        for r in results:
            score = r['recommendation'].get('overall_score', 50)
            recommendation = r['recommendation'].get('recommendation', 'HOLD')
            
            color = '#00C853' if recommendation == 'BUY' else '#FFC107' if recommendation == 'HOLD' else '#FF5252'
            
            chart_data.append({
                'Stock': r['stock'],
                'Score': score,
                'Recommendation': recommendation,
                'Color': color
            })
        
        df = pd.DataFrame(chart_data)
        
        fig = go.Figure(data=[
            go.Bar(
                x=df['Stock'],
                y=df['Score'],
                marker_color=df['Color'],
                text=df['Score'].round(1),
                textposition='auto',
                hovertemplate='<b>%{x}</b><br>Score: %{y:.1f}<br>%{customdata}<extra></extra>',
                customdata=df['Recommendation']
            )
        ])
        
        fig.update_layout(
            title="Stock Performance Scores",
            xaxis_title="Stock",
            yaxis_title="Score (0-100)",
            yaxis_range=[0, 100],
            height=400,
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("#### Detailed Cards")
        st.markdown("Expandable analysis with full metrics and reasoning")
        
        for r in results:
            stock = r['stock']
            rec = r['recommendation']
            analysis = r['analysis']
            
            recommendation = rec.get('recommendation', 'HOLD')
            score = rec.get('overall_score', 50)
            confidence = score
            
            if recommendation == 'BUY':
                color = "green"
                emoji = "🟢"
            elif recommendation == 'SELL':
                color = "red"
                emoji = "🔴"
            else:
                color = "orange"
                emoji = "🟡"
            
            with st.expander(f"{emoji} **{stock}** - {recommendation} (Score: {score:.1f})"):
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Recommendation", recommendation)
                with col2:
                    st.metric("Overall Score", f"{score:.1f}")
                with col3:
                    st.metric("Confidence", f"{confidence:.1f}%")
                with col4:
                    current_price = rec.get('current_price', 'N/A')
                    if current_price != 'N/A':
                        st.metric("Current Price", f"${current_price:.2f}" if isinstance(current_price, (int, float)) else current_price)
                    else:
                        st.metric("Current Price", "N/A")
                
                st.markdown("**Summary:**")
                st.info(rec.get('reasoning', 'No summary available'))
                
                st.markdown("---")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown("**📊 Fundamental Metrics**")
                    fundamental_score = rec.get('fundamental_score', 0)
                    st.write(f"**Score:** {fundamental_score:.1f}/100")
                    st.write(f"**P/E Ratio:** {rec.get('pe_ratio', 'N/A')}")
                    st.write(f"**P/B Ratio:** {rec.get('pb_ratio', 'N/A')}")
                    st.write(f"**ROE:** {rec.get('roe', 'N/A')}")
                    st.write(f"**Debt/Equity:** {rec.get('debt_equity', 'N/A')}")
                    st.write(f"**Profit Margin:** {rec.get('profit_margin', 'N/A')}")
                
                with col2:
                    st.markdown("**💰 Valuation & Size**")
                    st.write(f"**Market Cap:** {rec.get('market_cap', 'N/A')}")
                    st.write(f"**52W High:** {rec.get('week_52_high', 'N/A')}")
                    st.write(f"**52W Low:** {rec.get('week_52_low', 'N/A')}")
                    st.write(f"**Volume:** {rec.get('volume', 'N/A')}")
                    st.write(f"**Avg Volume:** {rec.get('avg_volume', 'N/A')}")
                    st.write(f"**Dividend Yield:** {rec.get('dividend_yield', 'N/A')}")
                
                with col3:
                    st.markdown("**💭 Sentiment & News**")
                    sentiment_score = rec.get('sentiment_score', 0)
                    st.write(f"**Score:** {sentiment_score:.1f}/100")
                    st.write(f"**Total Articles:** {rec.get('total_articles', 0)}")
                    st.write(f"**Avg Sentiment:** {rec.get('avg_sentiment', 0):.2f}")
                    
                    positive_count = rec.get('positive_articles', 0)
                    neutral_count = rec.get('neutral_articles', 0)
                    negative_count = rec.get('negative_articles', 0)
                    st.write(f"**Positive News:** {positive_count}")
                    st.write(f"**Neutral News:** {neutral_count}")
                    st.write(f"**Negative News:** {negative_count}")
                
                fundamental_data = analysis.get('fundamental', {})
                if fundamental_data and isinstance(fundamental_data, dict):
                    st.markdown("---")
                    st.markdown("**📈 Additional Financial Data**")
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        eps = fundamental_data.get('eps', 'N/A')
                        revenue = fundamental_data.get('revenue', 'N/A')
                        st.write(f"**EPS:** {eps}")
                        st.write(f"**Revenue:** {revenue}")
                    
                    with col2:
                        operating_margin = fundamental_data.get('operating_margin', 'N/A')
                        gross_margin = fundamental_data.get('gross_margin', 'N/A')
                        st.write(f"**Operating Margin:** {operating_margin}")
                        st.write(f"**Gross Margin:** {gross_margin}")
                    
                    with col3:
                        quick_ratio = fundamental_data.get('quick_ratio', 'N/A')
                        current_ratio = fundamental_data.get('current_ratio', 'N/A')
                        st.write(f"**Quick Ratio:** {quick_ratio}")
                        st.write(f"**Current Ratio:** {current_ratio}")
                
                sentiment_data = analysis.get('sentiment', {})
                if sentiment_data and isinstance(sentiment_data, dict):
                    news_items = sentiment_data.get('news_items', [])
                    if news_items:
                        st.markdown("---")
                        st.markdown("**📰 Recent News Headlines**")
                        
                        for i, news in enumerate(news_items[:5]):
                            title = news.get('title', 'No title')
                            sentiment_label = news.get('sentiment_label', 'neutral')
                            sentiment_icon = "🟢" if sentiment_label == 'positive' else "🔴" if sentiment_label == 'negative' else "🟡"
                            st.write(f"{sentiment_icon} {title}")
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📥 Export Report", use_container_width=True):
                report = {
                    'sector': st.session_state.sector,
                    'timestamp': datetime.now().isoformat(),
                    'risk_tolerance': st.session_state.risk_tolerance,
                    'analysis_balance': f"{balance}% sentiment / {100-balance}% fundamental",
                    'results': [{
                        'stock': r['stock'],
                        'recommendation': r['recommendation']['recommendation'],
                        'score': r['recommendation']['overall_score']
                    } for r in results]
                }
                
                import json
                report_json = json.dumps(report, indent=2)
                st.download_button(
                    "Download JSON",
                    report_json,
                    f"sector_analysis_{datetime.now().strftime('%Y%m%d')}.json",
                    "application/json"
                )
        
        with col2:
            if st.button("🔄 New Analysis", use_container_width=True):
                del st.session_state.analysis_results
                st.rerun()
    
    else:
        st.markdown("---")
        st.markdown("### 💡 How It Works")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **📰 Sentiment Analysis**
            - Fetches recent news articles
            - Analyzes sentiment using NLP
            - Identifies market mood
            - Provides sentiment score
            """)
        
        with col2:
            st.markdown("""
            **📊 Fundamental Analysis**
            - Evaluates financial metrics
            - Analyzes company fundamentals
            - Assesses valuation
            - Generates fundamental score
            """)
        
        st.markdown("""
        ### 📝 Tips
        - **Conservative**: Focus on fundamental analysis (0-30% sentiment)
        - **Moderate**: Balanced approach (40-60% sentiment)
        - **Aggressive**: Higher sentiment weight (70-100% sentiment)
        - Analyze multiple stocks to compare opportunities
        - Review detailed cards for in-depth insights
        """)
