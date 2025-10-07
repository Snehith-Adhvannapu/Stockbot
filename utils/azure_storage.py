import os
from datetime import datetime
from azure.storage.blob import BlobServiceClient, ContainerClient
from typing import Optional
import json

class AzureBlobStorage:
    """Azure Blob Storage integration for backing up trading logs"""
    
    def __init__(self):
        self.connection_string = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
        self.container_name = os.getenv('AZURE_STORAGE_CONTAINER_NAME', 'trading-logs')
        self.blob_service_client = None
        self.container_client = None
        self._initialize()
    
    def _initialize(self):
        """Initialize Azure Blob Storage connection"""
        if not self.connection_string or self.connection_string == 'your_connection_string_here':
            print("Azure Blob Storage not configured. Skipping cloud backup.")
            return
        
        try:
            self.blob_service_client = BlobServiceClient.from_connection_string(
                self.connection_string
            )
            
            self.container_client = self.blob_service_client.get_container_client(
                self.container_name
            )
            
            if not self.container_client.exists():
                self.container_client.create_container()
                print(f"Created Azure container: {self.container_name}")
            
            print("Azure Blob Storage initialized successfully")
        
        except Exception as e:
            print(f"Error initializing Azure Blob Storage: {e}")
            self.blob_service_client = None
            self.container_client = None
    
    def upload_log_file(self, file_path: str, blob_name: Optional[str] = None) -> bool:
        """Upload a log file to Azure Blob Storage"""
        if not self.container_client:
            return False
        
        try:
            if blob_name is None:
                blob_name = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{os.path.basename(file_path)}"
            
            with open(file_path, 'rb') as data:
                blob_client = self.container_client.upload_blob(
                    name=blob_name,
                    data=data,
                    overwrite=True
                )
            
            print(f"Uploaded {file_path} to Azure as {blob_name}")
            return True
        
        except Exception as e:
            print(f"Error uploading to Azure: {e}")
            return False
    
    def upload_json_data(self, data: dict, blob_name: str) -> bool:
        """Upload JSON data directly to Azure Blob Storage"""
        if not self.container_client:
            return False
        
        try:
            json_data = json.dumps(data, indent=2)
            
            blob_client = self.container_client.upload_blob(
                name=blob_name,
                data=json_data,
                overwrite=True
            )
            
            print(f"Uploaded JSON data to Azure as {blob_name}")
            return True
        
        except Exception as e:
            print(f"Error uploading JSON to Azure: {e}")
            return False
    
    def backup_trading_logs(self, log_directory: str = 'trading_logs') -> int:
        """Backup all trading logs to Azure"""
        if not self.container_client:
            return 0
        
        uploaded_count = 0
        
        try:
            for filename in os.listdir(log_directory):
                if filename.endswith('.jsonl'):
                    file_path = os.path.join(log_directory, filename)
                    blob_name = f"backups/{datetime.now().strftime('%Y-%m-%d')}/{filename}"
                    
                    if self.upload_log_file(file_path, blob_name):
                        uploaded_count += 1
            
            print(f"Backed up {uploaded_count} log files to Azure")
            return uploaded_count
        
        except Exception as e:
            print(f"Error backing up logs: {e}")
            return uploaded_count
    
    def list_backups(self, prefix: str = '') -> list:
        """List all backups in Azure Blob Storage"""
        if not self.container_client:
            return []
        
        try:
            blobs = self.container_client.list_blobs(name_starts_with=prefix)
            return [blob.name for blob in blobs]
        
        except Exception as e:
            print(f"Error listing backups: {e}")
            return []
    
    def download_backup(self, blob_name: str, download_path: str) -> bool:
        """Download a backup from Azure Blob Storage"""
        if not self.container_client:
            return False
        
        try:
            blob_client = self.container_client.get_blob_client(blob_name)
            
            with open(download_path, 'wb') as download_file:
                download_file.write(blob_client.download_blob().readall())
            
            print(f"Downloaded {blob_name} to {download_path}")
            return True
        
        except Exception as e:
            print(f"Error downloading backup: {e}")
            return False
    
    def is_configured(self) -> bool:
        """Check if Azure Blob Storage is properly configured"""
        return self.blob_service_client is not None and self.container_client is not None
