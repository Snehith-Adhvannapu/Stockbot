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
    "🖥️ IT & Tech": ["TCS", "INFY", "HCLTECH", "WIPRO", "TECHM"],
    "🏦 Banking": ["HDFCBANK", "ICICIBANK", "SBI", "KOTAKBANK", "AXISBANK"],
    "🚗 Auto": ["MARUTI", "TATAMOTORS", "M&M", "BAJAJ-AUTO", "EICHERMOT"],
    "⚗️ Pharma": ["SUNPHARMA", "DRREDDY", "CIPLA", "DIVISLAB", "BIOCON"],
    "🌿 Green Energy": ["ADANIGREEN", "SUZLON", "TATAPOWER", "NTPC", "POWERGRID"],
    "🏭 Diversified": ["RELIANCE", "ITC", "HINDUNILVR", "LT", "ASIANPAINT"]
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
    
    st.markdown("### 1. Choose Your Sector")
    st.markdown("Select from predefined sectors:")
    
    selected_sector = st.selectbox(
        "Sector",
        options=list(SECTORS.keys()),
        label_visibility="collapsed"
    )
    
    stocks_in_sector = SECTORS[selected_sector]
    st.caption(f"**Stocks:** {', '.join(stocks_in_sector)}")
    
    st.markdown("---")
    
    st.markdown("### 2. Set Analysis Balance")
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
    
    st.markdown("### 3. Advanced Options")
    
    col1, col2 = st.columns(2)
    
    with col1:
        stock_count = st.slider(
            "Stock Count",
            min_value=3,
            max_value=10,
            value=5,
            help="Analyze 3-10 stocks per sector"
        )
        st.caption("Analyze 3-10 stocks per sector")
    
    with col2:
        risk_tolerance = st.select_slider(
            "Risk Tolerance",
            options=["Conservative", "Moderate", "Aggressive"],
            value="Moderate"
        )
        st.caption("Select your risk profile")
    
    st.markdown("---")
    
    analyze_button = st.button("🔍 Analyze Sector", type="primary", use_container_width=True)
    
    if analyze_button:
        stocks_to_analyze = stocks_in_sector[:stock_count]
        
        with st.spinner(f"Analyzing {len(stocks_to_analyze)} stocks from {selected_sector}..."):
            try:
                screening_agent, fundamental_agent, sentiment_agent, aggregator_agent, data_normalizer = initialize_agents()
                cache_manager = get_cache_manager()
                
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                all_results = []
                
                for idx, stock in enumerate(stocks_to_analyze):
                    symbol = f"{stock}.NS"
                    
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
                st.session_state.sector = selected_sector
                st.session_state.risk_tolerance = risk_tolerance
                
            except Exception as e:
                st.error(f"Analysis failed: {str(e)}")
                return
    
    if 'analysis_results' in st.session_state and st.session_state.analysis_results:
        results = st.session_state.analysis_results
        
        st.markdown("---")
        st.markdown("### 4. Review Results")
        
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
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Recommendation", recommendation)
                with col2:
                    st.metric("Score", f"{score:.1f}")
                with col3:
                    st.metric("Confidence", f"{confidence:.1f}%")
                
                st.markdown("**Summary:**")
                st.info(rec.get('reasoning', 'No summary available'))
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**📊 Fundamental Analysis**")
                    fundamental_score = rec.get('fundamental_score', 0)
                    st.write(f"Score: {fundamental_score:.1f}/100")
                    
                    st.write(f"P/E Ratio: {rec.get('pe_ratio', 'N/A')}")
                    st.write(f"Market Cap: {rec.get('market_cap', 'N/A')}")
                    st.write(f"ROE: {rec.get('roe', 'N/A')}")
                
                with col2:
                    st.markdown("**💭 Sentiment Analysis**")
                    sentiment_score = rec.get('sentiment_score', 0)
                    st.write(f"Score: {sentiment_score:.1f}/100")
                    st.write(f"News Articles: {rec.get('total_articles', 0)}")
                    st.write(f"Avg Sentiment: {rec.get('avg_sentiment', 0):.2f}")
        
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
