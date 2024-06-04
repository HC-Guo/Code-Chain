from azure.storage.blob import BlobServiceClient
from azure.core.exceptions import ResourceNotFoundError

import os

from app.config import Settings

class AzureBlobStorage:

    def __init__(self):
        setting = Settings()
        self.blob_service_client = BlobServiceClient.from_connection_string(setting.azure_conn_string)
        self.container_name = 'hongcheng'  
        self.container_client = self.blob_service_client.get_container_client(self.container_name)

    def save(self, file_path: str, content: str, repo_name: str):
        # 在文件路径前添加 'code_chain/' 前缀
        blob_name = os.path.join('code_chain', repo_name, file_path)
        self.upload_blob(blob_name, content)
        return blob_name
    
    def upload_blob(self, blob_name, data, overwrite=True):
        blob_client = self.blob_service_client.get_blob_client(self.container_name, blob_name)  # 使用 self.container_name
        blob_client.upload_blob(data, overwrite=overwrite)

    def download_blob(self, blob_name):
        blob_client = self.blob_service_client.get_blob_client(self.container_name, blob_name)
        download_stream = blob_client.download_blob().readall()
        return download_stream

    def exists(self, blob_name):
        blob_client = self.blob_service_client.get_blob_client(self.container_name, blob_name)
        try:
            blob_client.get_blob_properties()
            return True
        except ResourceNotFoundError:
            return False