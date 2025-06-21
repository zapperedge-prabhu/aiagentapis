import logging
from urllib.parse import urlparse  # ✅ REQUIRED for parsing blob URLs
from azure.storage.blob import BlobServiceClient, BlobClient  # ⬅️ added BlobClient
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

    def _is_sas_url(self, url: str) -> bool:
        return url.startswith("https://") and "?" in url

    def download_blob_content(self, blob_url_or_path):
        """
        Download content from Azure Blob Storage

        Args:
            blob_url_or_path (str): Blob URL or path in format container/blob_name or full URL

        Returns:
            bytes: The blob content
        """
        try:
            if self._is_sas_url(blob_url_or_path):
                blob_client = BlobClient.from_blob_url(blob_url_or_path)
            elif blob_url_or_path.startswith("https://"):
                # Parse URL manually to extract container/blob
                parsed = urlparse(blob_url_or_path)
                path_parts = parsed.path.lstrip("/").split("/", 1)
                if len(path_parts) != 2:
                    raise ValueError("Invalid blob URL format: missing container/blob_name")
                container_name, blob_name = path_parts
                blob_client = self.blob_service_client.get_blob_client(container=container_name, blob=blob_name)
            else:
                # fallback for container/blob_name format
                parts = blob_url_or_path.split("/", 1)
                if len(parts) != 2:
                    raise ValueError("Invalid blob path format. Expected container/blob_name")
                container_name, blob_name = parts
                blob_client = self.blob_service_client.get_blob_client(container=container_name, blob=blob_name)

            blob_data = blob_client.download_blob()
            content = blob_data.readall()

            logger.info(f"Successfully downloaded blob: {blob_client.container_name}/{blob_client.blob_name}")
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
            if self._is_sas_url(blob_url_or_path):
                blob_client = BlobClient.from_blob_url(blob_url_or_path)
            elif blob_url_or_path.startswith("https://"):
                parsed = urlparse(blob_url_or_path)
                path_parts = parsed.path.lstrip("/").split("/", 1)
                if len(path_parts) != 2:
                    raise ValueError("Invalid blob URL format: missing container/blob_name")
                container_name, blob_name = path_parts
                blob_client = self.blob_service_client.get_blob_client(container=container_name, blob=blob_name)
            else:
                parts = blob_url_or_path.split("/", 1)
                if len(parts) != 2:
                    raise ValueError("Invalid blob path format. Expected container/blob_name")
                container_name, blob_name = parts
                blob_client = self.blob_service_client.get_blob_client(container=container_name, blob=blob_name)

            properties = blob_client.get_blob_properties()
            
            return {
                'content_type': properties.content_settings.content_type,
                'size': properties.size,
                'last_modified': properties.last_modified,
                'name': blob_client.blob_name  # ⬅️ consistent with above
            }
            
        except Exception as e:
            logger.error(f"Error getting blob properties {blob_url_or_path}: {e}")
            raise
