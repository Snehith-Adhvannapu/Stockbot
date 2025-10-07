import os
import requests
from datetime import datetime
from typing import Dict, Optional
import json

class AzureScheduler:
    """Azure Functions integration for scheduled tasks"""
    
    def __init__(self):
        self.functions_url = os.getenv('AZURE_FUNCTIONS_URL')
        self.configured = False
        self._initialize()
    
    def _initialize(self):
        """Initialize Azure Functions connection"""
        if not self.functions_url or self.functions_url == 'your_azure_functions_url_here':
            print("Azure Functions not configured. Scheduled tasks will run locally.")
            return
        
        self.configured = True
        print("Azure Functions scheduler initialized")
    
    def trigger_market_scan(self, symbols: list) -> Dict:
        """Trigger a market scan via Azure Functions"""
        if not self.configured:
            return {'success': False, 'error': 'Azure Functions not configured'}
        
        try:
            payload = {
                'action': 'market_scan',
                'symbols': symbols,
                'timestamp': datetime.now().isoformat()
            }
            
            response = requests.post(
                f"{self.functions_url}/api/market-scan",
                json=payload,
                timeout=30
            )
            
            response.raise_for_status()
            return {'success': True, 'data': response.json()}
        
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def schedule_daily_report(self, email: str, portfolio_data: dict) -> Dict:
        """Schedule a daily portfolio report via Azure Functions"""
        if not self.configured:
            return {'success': False, 'error': 'Azure Functions not configured'}
        
        try:
            payload = {
                'action': 'daily_report',
                'email': email,
                'portfolio_data': portfolio_data,
                'timestamp': datetime.now().isoformat()
            }
            
            response = requests.post(
                f"{self.functions_url}/api/daily-report",
                json=payload,
                timeout=30
            )
            
            response.raise_for_status()
            return {'success': True, 'data': response.json()}
        
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def trigger_risk_check(self, portfolio_value: float, positions: list) -> Dict:
        """Trigger a risk analysis via Azure Functions"""
        if not self.configured:
            return {'success': False, 'error': 'Azure Functions not configured'}
        
        try:
            payload = {
                'action': 'risk_check',
                'portfolio_value': portfolio_value,
                'positions': positions,
                'timestamp': datetime.now().isoformat()
            }
            
            response = requests.post(
                f"{self.functions_url}/api/risk-check",
                json=payload,
                timeout=30
            )
            
            response.raise_for_status()
            return {'success': True, 'data': response.json()}
        
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def schedule_backup(self) -> Dict:
        """Trigger a backup job via Azure Functions"""
        if not self.configured:
            return {'success': False, 'error': 'Azure Functions not configured'}
        
        try:
            payload = {
                'action': 'backup',
                'timestamp': datetime.now().isoformat()
            }
            
            response = requests.post(
                f"{self.functions_url}/api/backup",
                json=payload,
                timeout=60
            )
            
            response.raise_for_status()
            return {'success': True, 'data': response.json()}
        
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def is_configured(self) -> bool:
        """Check if Azure Functions is properly configured"""
        return self.configured
