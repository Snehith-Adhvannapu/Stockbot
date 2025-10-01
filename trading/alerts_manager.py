from typing import Dict, List, Optional
from datetime import datetime
import json
from pathlib import Path

class AlertsManager:
    """Manage trading alerts and notifications"""
    
    def __init__(self, alerts_file: str = "trading_logs/alerts.jsonl"):
        self.alerts_file = Path(alerts_file)
        self.alerts_file.parent.mkdir(exist_ok=True)
        self.active_alerts = []
    
    def create_price_alert(
        self,
        symbol: str,
        target_price: float,
        condition: str = 'above',
        alert_type: str = 'price'
    ) -> Dict:
        """
        Create a price alert
        
        Args:
            symbol: Stock symbol
            target_price: Target price to trigger alert
            condition: 'above' or 'below'
            alert_type: Type of alert
        """
        alert = {
            'id': f"alert_{datetime.now().timestamp()}",
            'symbol': symbol,
            'alert_type': alert_type,
            'target_price': target_price,
            'condition': condition,
            'status': 'active',
            'created_at': datetime.now().isoformat(),
            'triggered_at': None
        }
        
        self.active_alerts.append(alert)
        self._save_alert(alert)
        
        return alert
    
    def create_volume_alert(
        self,
        symbol: str,
        volume_threshold: int,
        condition: str = 'above'
    ) -> Dict:
        """Create a volume alert"""
        alert = {
            'id': f"alert_{datetime.now().timestamp()}",
            'symbol': symbol,
            'alert_type': 'volume',
            'volume_threshold': volume_threshold,
            'condition': condition,
            'status': 'active',
            'created_at': datetime.now().isoformat(),
            'triggered_at': None
        }
        
        self.active_alerts.append(alert)
        self._save_alert(alert)
        
        return alert
    
    def create_signal_alert(
        self,
        symbol: str,
        signal_type: str,
        strategy: str
    ) -> Dict:
        """Create a trading signal alert"""
        alert = {
            'id': f"alert_{datetime.now().timestamp()}",
            'symbol': symbol,
            'alert_type': 'signal',
            'signal_type': signal_type,
            'strategy': strategy,
            'status': 'active',
            'created_at': datetime.now().isoformat(),
            'triggered_at': None
        }
        
        self.active_alerts.append(alert)
        self._save_alert(alert)
        
        return alert
    
    def check_price_alerts(self, symbol: str, current_price: float) -> List[Dict]:
        """Check if any price alerts should be triggered"""
        triggered = []
        
        for alert in self.active_alerts:
            if (alert['alert_type'] == 'price' and 
                alert['symbol'] == symbol and 
                alert['status'] == 'active'):
                
                if alert['condition'] == 'above' and current_price >= alert['target_price']:
                    alert['status'] = 'triggered'
                    alert['triggered_at'] = datetime.now().isoformat()
                    alert['trigger_price'] = current_price
                    triggered.append(alert)
                    self._save_alert(alert)
                
                elif alert['condition'] == 'below' and current_price <= alert['target_price']:
                    alert['status'] = 'triggered'
                    alert['triggered_at'] = datetime.now().isoformat()
                    alert['trigger_price'] = current_price
                    triggered.append(alert)
                    self._save_alert(alert)
        
        return triggered
    
    def check_volume_alerts(self, symbol: str, current_volume: int) -> List[Dict]:
        """Check if any volume alerts should be triggered"""
        triggered = []
        
        for alert in self.active_alerts:
            if (alert['alert_type'] == 'volume' and 
                alert['symbol'] == symbol and 
                alert['status'] == 'active'):
                
                if alert['condition'] == 'above' and current_volume >= alert['volume_threshold']:
                    alert['status'] = 'triggered'
                    alert['triggered_at'] = datetime.now().isoformat()
                    alert['trigger_volume'] = current_volume
                    triggered.append(alert)
                    self._save_alert(alert)
                
                elif alert['condition'] == 'below' and current_volume <= alert['volume_threshold']:
                    alert['status'] = 'triggered'
                    alert['triggered_at'] = datetime.now().isoformat()
                    alert['trigger_volume'] = current_volume
                    triggered.append(alert)
                    self._save_alert(alert)
        
        return triggered
    
    def trigger_signal_alert(self, symbol: str, signal: str, strategy: str) -> List[Dict]:
        """Trigger signal-based alerts"""
        triggered = []
        
        for alert in self.active_alerts:
            if (alert['alert_type'] == 'signal' and 
                alert['symbol'] == symbol and 
                alert['signal_type'] == signal and
                alert['status'] == 'active'):
                
                alert['status'] = 'triggered'
                alert['triggered_at'] = datetime.now().isoformat()
                triggered.append(alert)
                self._save_alert(alert)
        
        return triggered
    
    def get_active_alerts(self, symbol: Optional[str] = None) -> List[Dict]:
        """Get all active alerts, optionally filtered by symbol"""
        if symbol:
            return [a for a in self.active_alerts if a['symbol'] == symbol and a['status'] == 'active']
        return [a for a in self.active_alerts if a['status'] == 'active']
    
    def get_triggered_alerts(self, limit: int = 50) -> List[Dict]:
        """Get recently triggered alerts"""
        if not self.alerts_file.exists():
            return []
        
        alerts = []
        with open(self.alerts_file, 'r') as f:
            for line in f.readlines()[-limit:]:
                try:
                    alert = json.loads(line.strip())
                    if alert['status'] == 'triggered':
                        alerts.append(alert)
                except:
                    continue
        
        return alerts
    
    def delete_alert(self, alert_id: str) -> bool:
        """Delete an alert"""
        self.active_alerts = [a for a in self.active_alerts if a['id'] != alert_id]
        return True
    
    def _save_alert(self, alert: Dict):
        """Save alert to file"""
        try:
            with open(self.alerts_file, 'a') as f:
                f.write(json.dumps(alert) + '\n')
        except Exception as e:
            print(f"Error saving alert: {e}")
