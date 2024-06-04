import boto3
import os
import mimetypes
from botocore.client import Config

from app.config import Settings

setting = Settings()

class CloudflareR2:
    R2_BUCKET_NAME = setting.r2_bucket_name
    R2_ENDPOINT = setting.r2_endpoint
    R2_ACCESS_KEY = setting.r2_access_key
    R2_SECRET_KEY = setting.r2_secret_key

    def __init__(self):
        self.s3 = boto3.client('s3', 
                               endpoint_url=self.R2_ENDPOINT, 
                               aws_access_key_id=self.R2_ACCESS_KEY, 
                               aws_secret_access_key=self.R2_SECRET_KEY,
                               config=Config(signature_version='s3v4'))

    def save(self, file_path: str, content: str, repo_name: str):
        key = os.path.join(repo_name, file_path)
        content_type = mimetypes.guess_type(file_path)[0] or 'application/octet-stream'

        self.s3.put_object(
            Body=content, 
            Bucket=self.R2_BUCKET_NAME, 
            Key=key, 
            ContentType=content_type)

        return key
