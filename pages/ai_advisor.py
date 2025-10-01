import streamlit as st
import pandas as pd
import time
from datetime import datetime

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
    st.title("🧠 AI Stock Advisor")
    st.markdown("Multi-agent stock analysis combining sentiment and fundamental research")
    
    st.markdown("### 📊 Enter Stock Symbol")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        symbol_input = st.text_input(
            "Stock Symbol",
            value="AAPL",
            max_chars=10,
            placeholder="e.g., AAPL, MSFT, GOOGL"
        ).upper()
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        analyze_button = st.button("🔍 Analyze", type="primary", use_container_width=True)
    
    st.markdown("### ⚙️ Analysis Configuration")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        sentiment_weight = st.slider(
            "Sentiment Weight",
            min_value=0.0,
            max_value=1.0,
            value=0.4,
            step=0.1,
            help="Weight given to sentiment analysis"
        )
    
    with col2:
        fundamental_weight = st.slider(
            "Fundamental Weight",
            min_value=0.0,
            max_value=1.0,
            value=0.6,
            step=0.1,
            help="Weight given to fundamental analysis"
        )
    
    with col3:
        total_weight = sentiment_weight + fundamental_weight
        if abs(total_weight - 1.0) > 0.01:
            st.warning(f"⚠️ Total: {total_weight:.1f}")
        else:
            st.success(f"✅ Total: {total_weight:.1f}")
    
    if analyze_button and symbol_input:
        with st.spinner(f"Analyzing {symbol_input}..."):
            try:
                screening_agent, fundamental_agent, sentiment_agent, aggregator_agent, data_normalizer = initialize_agents()
                cache_manager = get_cache_manager()
                
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                status_text.text("🔍 Running sentiment analysis...")
                progress_bar.progress(25)
                sentiment_result = sentiment_agent.analyze(symbol_input)
                time.sleep(0.5)
                
                status_text.text("📊 Performing fundamental analysis...")
                progress_bar.progress(50)
                fundamental_result = fundamental_agent.analyze(symbol_input)
                time.sleep(0.5)
                
                status_text.text("🤖 Aggregating results...")
                progress_bar.progress(75)
                
                analysis_results = {
                    'symbol': symbol_input,
                    'sentiment': sentiment_result,
                    'fundamental': fundamental_result,
                    'weights': {
                        'sentiment': sentiment_weight,
                        'fundamental': fundamental_weight
                    }
                }
                
                final_recommendation = aggregator_agent.aggregate(analysis_results)
                progress_bar.progress(100)
                status_text.text("✅ Analysis complete!")
                
                time.sleep(0.5)
                progress_bar.empty()
                status_text.empty()
                
                st.session_state.analysis_results = analysis_results
                st.session_state.final_recommendation = final_recommendation
                
            except Exception as e:
                st.error(f"Analysis failed: {str(e)}")
                st.exception(e)
                return
    
    if 'final_recommendation' in st.session_state:
        recommendation = st.session_state.final_recommendation
        analysis = st.session_state.analysis_results
        
        st.markdown("---")
        st.markdown("### 📊 Analysis Results")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            action = recommendation.get('recommendation', 'HOLD')
            if action == 'BUY':
                st.success(f"### 🟢 {action}")
            elif action == 'SELL':
                st.error(f"### 🔴 {action}")
            else:
                st.info(f"### 🟡 {action}")
        
        with col2:
            confidence = recommendation.get('confidence', 0) * 100
            st.metric("Confidence", f"{confidence:.1f}%")
        
        with col3:
            score = recommendation.get('score', 0) * 10
            st.metric("Overall Score", f"{score:.1f}/10")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 💭 Sentiment Analysis")
            sentiment_data = analysis.get('sentiment', {})
            
            if sentiment_data and 'error' not in sentiment_data:
                sentiment_score = sentiment_data.get('sentiment_score', 0)
                
                if sentiment_score > 0.2:
                    st.success(f"**Score:** {sentiment_score:.2f} (Positive)")
                elif sentiment_score < -0.2:
                    st.error(f"**Score:** {sentiment_score:.2f} (Negative)")
                else:
                    st.info(f"**Score:** {sentiment_score:.2f} (Neutral)")
                
                st.write(f"**News Articles:** {sentiment_data.get('num_articles', 0)}")
                st.write(f"**Avg Sentiment:** {sentiment_data.get('avg_sentiment', 0):.2f}")
                
                if sentiment_data.get('summary'):
                    with st.expander("View Summary"):
                        st.write(sentiment_data['summary'])
            else:
                st.warning("Sentiment data unavailable")
        
        with col2:
            st.markdown("#### 📈 Fundamental Analysis")
            fundamental_data = analysis.get('fundamental', {})
            
            if fundamental_data and 'error' not in fundamental_data:
                fundamental_score = fundamental_data.get('fundamental_score', 0)
                
                if fundamental_score > 6:
                    st.success(f"**Score:** {fundamental_score:.1f}/10 (Strong)")
                elif fundamental_score > 4:
                    st.info(f"**Score:** {fundamental_score:.1f}/10 (Moderate)")
                else:
                    st.warning(f"**Score:** {fundamental_score:.1f}/10 (Weak)")
                
                metrics = fundamental_data.get('metrics', {})
                if metrics:
                    st.write(f"**P/E Ratio:** {metrics.get('pe_ratio', 'N/A')}")
                    st.write(f"**EPS:** ${metrics.get('eps', 'N/A')}")
                    st.write(f"**Market Cap:** ${metrics.get('market_cap', 'N/A')}")
            else:
                st.warning("Fundamental data unavailable")
        
        st.markdown("---")
        st.markdown("### 📝 Recommendation Summary")
        
        summary = recommendation.get('summary', 'No summary available')
        st.info(summary)
        
        if recommendation.get('reasoning'):
            with st.expander("📋 Detailed Reasoning"):
                for reason in recommendation['reasoning']:
                    st.write(f"• {reason}")
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📥 Export Report", use_container_width=True):
                report = {
                    'symbol': analysis['symbol'],
                    'timestamp': datetime.now().isoformat(),
                    'recommendation': recommendation['recommendation'],
                    'confidence': recommendation['confidence'],
                    'score': recommendation['score'],
                    'analysis': analysis
                }
                
                import json
                report_json = json.dumps(report, indent=2)
                st.download_button(
                    "Download JSON",
                    report_json,
                    f"{analysis['symbol']}_analysis_{datetime.now().strftime('%Y%m%d')}.json",
                    "application/json"
                )
        
        with col2:
            if st.button("🔄 New Analysis", use_container_width=True):
                del st.session_state.analysis_results
                del st.session_state.final_recommendation
                st.rerun()
    
    else:
        st.markdown("---")
        st.markdown("### 🔍 How It Works")
        
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
        ### 💡 Tips
        - Adjust weights to prioritize different analysis types
        - Sentiment analysis works best for trending stocks
        - Fundamental analysis is better for long-term decisions
        - Use both for comprehensive insights
        """)
