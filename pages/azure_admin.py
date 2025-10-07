import streamlit as st
from datetime import datetime
from utils.azure_storage import AzureBlobStorage
from utils.azure_scheduler import AzureScheduler

def show():
    st.title("☁️ Azure Cloud Services")
    st.markdown("Manage your cloud backups and scheduled tasks")
    
    tab1, tab2 = st.tabs(["📦 Blob Storage (Backups)", "⚡ Functions (Scheduled Tasks)"])
    
    with tab1:
        st.markdown("### Azure Blob Storage - Log Backups")
        
        azure_storage = AzureBlobStorage()
        
        if azure_storage.is_configured():
            st.success("✅ Azure Blob Storage is connected and ready")
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("📤 Backup Logs Now", type="primary", use_container_width=True):
                    with st.spinner("Uploading logs to Azure..."):
                        count = azure_storage.backup_trading_logs('trading_logs')
                        if count > 0:
                            st.success(f"Successfully backed up {count} log files to Azure!")
                        else:
                            st.info("No logs to backup or backup failed")
            
            with col2:
                if st.button("📋 List Backups", use_container_width=True):
                    with st.spinner("Fetching backup list..."):
                        backups = azure_storage.list_backups('backups/')
                        
                        if backups:
                            st.markdown(f"**Found {len(backups)} backups:**")
                            for backup in backups[:10]:
                                st.text(f"• {backup}")
                            
                            if len(backups) > 10:
                                st.info(f"...and {len(backups) - 10} more")
                        else:
                            st.info("No backups found in Azure")
            
            st.markdown("---")
            st.markdown("### Backup Status")
            
            st.info("""
            **Auto-Backup is ENABLED** 
            
            Your trading logs are automatically backed up to Azure Blob Storage in real-time:
            - ✅ Every trade is backed up immediately
            - ✅ All decisions are logged to the cloud
            - ✅ Performance metrics are saved
            - ✅ Errors are tracked
            
            Your data is safe even if this server goes down!
            """)
            
        else:
            st.warning("⚠️ Azure Blob Storage is NOT configured")
            
            st.markdown("""
            ### How to Set Up Azure Blob Storage:
            
            1. **Create an Azure Storage Account**
               - Go to [Azure Portal](https://portal.azure.com)
               - Create a new Storage Account (Free tier available)
            
            2. **Get Connection String**
               - In your Storage Account, go to "Access Keys"
               - Copy the connection string
            
            3. **Update .env file**
               ```
               AZURE_STORAGE_CONNECTION_STRING=your_connection_string_here
               AZURE_STORAGE_CONTAINER_NAME=trading-logs
               ```
            
            4. **Restart the app**
               - Your logs will automatically backup to Azure!
            """)
            
            with st.expander("Why use Azure Blob Storage?"):
                st.markdown("""
                **Benefits:**
                - 📦 **Unlimited storage** - Never lose your trading history
                - 🔒 **Secure** - Enterprise-grade security
                - 🌍 **Accessible anywhere** - Access logs from any device
                - 💰 **Free tier** - First 5GB free forever
                - ⚡ **Fast** - Lightning-fast uploads and downloads
                - 🔄 **Automatic** - Backs up every trade in real-time
                """)
    
    with tab2:
        st.markdown("### Azure Functions - Scheduled Tasks")
        
        azure_scheduler = AzureScheduler()
        
        if azure_scheduler.is_configured():
            st.success("✅ Azure Functions is connected and ready")
            
            st.markdown("### Available Scheduled Tasks")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### 🔍 Market Scan")
                symbols_input = st.text_input(
                    "Symbols to scan:",
                    value="AAPL,MSFT,GOOGL",
                    key="scan_symbols"
                )
                
                if st.button("Trigger Market Scan", use_container_width=True):
                    symbols = [s.strip() for s in symbols_input.split(',')]
                    with st.spinner("Running market scan..."):
                        result = azure_scheduler.trigger_market_scan(symbols)
                        
                        if result.get('success'):
                            st.success("Market scan completed!")
                            st.json(result.get('data'))
                        else:
                            st.error(f"Scan failed: {result.get('error')}")
            
            with col2:
                st.markdown("#### 💾 Backup Job")
                
                if st.button("Trigger Cloud Backup", use_container_width=True):
                    with st.spinner("Starting backup job..."):
                        result = azure_scheduler.schedule_backup()
                        
                        if result.get('success'):
                            st.success("Backup job started!")
                            st.json(result.get('data'))
                        else:
                            st.error(f"Backup failed: {result.get('error')}")
            
            st.markdown("---")
            
            st.markdown("#### 📊 Daily Report")
            
            email = st.text_input("Your email:", placeholder="you@example.com")
            
            if st.button("Schedule Daily Report", use_container_width=True):
                if email:
                    portfolio_data = {
                        'value': 100000,
                        'timestamp': datetime.now().isoformat()
                    }
                    
                    with st.spinner("Scheduling report..."):
                        result = azure_scheduler.schedule_daily_report(email, portfolio_data)
                        
                        if result.get('success'):
                            st.success(f"Daily report will be sent to {email}!")
                        else:
                            st.error(f"Failed: {result.get('error')}")
                else:
                    st.warning("Please enter your email")
            
        else:
            st.warning("⚠️ Azure Functions is NOT configured")
            
            st.markdown("""
            ### How to Set Up Azure Functions:
            
            1. **Create an Azure Function App**
               - Go to [Azure Portal](https://portal.azure.com)
               - Create a new Function App (Consumption plan is free)
            
            2. **Get Function URL**
               - Once deployed, copy your function app URL
            
            3. **Update .env file**
               ```
               AZURE_FUNCTIONS_URL=https://your-function-app.azurewebsites.net
               ```
            
            4. **Restart the app**
               - You can now schedule automated tasks!
            """)
            
            with st.expander("Why use Azure Functions?"):
                st.markdown("""
                **Benefits:**
                - ⚡ **Serverless** - No servers to manage
                - 💰 **Pay per use** - Only pay when functions run
                - 🔄 **Automated tasks** - Schedule market scans, reports, backups
                - 📧 **Notifications** - Get email/SMS alerts
                - 🌍 **Global** - Run anywhere in the world
                - 🆓 **Free tier** - 1 million executions/month free
                """)
    
    st.markdown("---")
    st.markdown("### 💡 Quick Tips")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("""
        **Azure Blob Storage:**
        - Free 5GB storage
        - Perfect for log backups
        - Access from anywhere
        """)
    
    with col2:
        st.info("""
        **Azure Functions:**
        - 1M free executions/month
        - Automate market analysis
        - Send daily reports
        """)
