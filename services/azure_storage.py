import logging
from azure.storage.blob import BlobServiceClient
from azure.core.exceptions import ResourceNotFoundError
from config import AZURE_STORAGE_CONNECTION_STRING

logger = logging.getLogger(__name__)

class AzureBlobStorage:
    def __init__(self):
        """Initialize Azure Blob Storage client"""
        try:
            self.blob_service_client = BlobServiceClient.from_connection_string(
                AZURE_STORAGE_CONNECTION_STRING
            )
            logger.info("Azure Blob Storage client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Azure Blob Storage client: {e}")
            raise

    def download_blob_content(self, blob_url_or_path):
        """
        Download content from Azure Blob Storage
        
        Args:
            blob_url_or_path (str): Blob URL or path in format container/blob_name
            
        Returns:
            bytes: The blob content
        """
        try:
            # Parse blob URL - only full URLs are supported
            if not blob_url_or_path.startswith('https://'):
                raise ValueError("Invalid file path. Only full Azure Blob Storage URLs are supported. Format: https://storagetest12344.blob.core.windows.net/container/filename.ext")
            
            # Extract container and blob name from URL
            # Format: https://account.blob.core.windows.net/container/path/to/blob
            url_parts = blob_url_or_path.split('/')
            if len(url_parts) < 5:
                raise ValueError("Invalid Azure Blob Storage URL format")
            container_name = url_parts[3]  # First part after domain
            blob_name = '/'.join(url_parts[4:])  # Remaining parts as blob path
            
            # Get blob client and download content
            blob_client = self.blob_service_client.get_blob_client(
                container=container_name, 
                blob=blob_name
            )
            
            blob_data = blob_client.download_blob()
            content = blob_data.readall()
            
            logger.info(f"Successfully downloaded blob: {container_name}/{blob_name}")
            return content
            
        except ResourceNotFoundError:
            logger.error(f"Blob not found: {blob_url_or_path}")
            raise FileNotFoundError(f"Blob not found: {blob_url_or_path}")
        except Exception as e:
            logger.error(f"Error downloading blob {blob_url_or_path}: {e}")
            raise

    def get_blob_properties(self, blob_url_or_path):
        """
        Get blob properties including content type and size
        
        Args:
            blob_url_or_path (str): Blob URL or path
            
        Returns:
            dict: Blob properties
        """
        try:
            # Parse blob URL - only full URLs are supported
            if not blob_url_or_path.startswith('https://'):
                raise ValueError("Invalid file path. Only full Azure Blob Storage URLs are supported. Format: https://storagetest12344.blob.core.windows.net/container/filename.ext")
            
            # Extract container and blob name from URL
            # Format: https://account.blob.core.windows.net/container/path/to/blob
            url_parts = blob_url_or_path.split('/')
            if len(url_parts) < 5:
                raise ValueError("Invalid Azure Blob Storage URL format")
            container_name = url_parts[3]  # First part after domain
            blob_name = '/'.join(url_parts[4:])  # Remaining parts as blob path
            
            blob_client = self.blob_service_client.get_blob_client(
                container=container_name, 
                blob=blob_name
            )
            
            properties = blob_client.get_blob_properties()
            
            return {
                'content_type': properties.content_settings.content_type,
                'size': properties.size,
                'last_modified': properties.last_modified,
                'name': blob_name
            }
            
        except Exception as e:
            logger.error(f"Error getting blob properties {blob_url_or_path}: {e}")
            raise
