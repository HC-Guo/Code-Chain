import os
from dotenv import load_dotenv, find_dotenv

class Settings:
    def __init__(self):
        load_dotenv(find_dotenv())
        self.github_api_tokens = self.load_github_tokens()
        self.r2_bucket_name = os.getenv("R2_BUCKET_NAME")
        self.r2_endpoint = os.getenv("R2_ENDPOINT")
        self.r2_access_key = os.getenv("R2_ACCESS_KEY")
        self.r2_secret_key = os.getenv("R2_SECRET_KEY")
        self.mongodb_url = os.getenv("MONGODB_URL")
        self.mongodb_db_name = "tongyi"
        self.mongo_collection_name = "python"
        self.azure_conn_string = os.getenv("AZURE_CONN_STRING")
        self.github_api_token = os.getenv("GITHUB_API_TOKEN_0")

    def load_github_tokens(self):
        tokens = []
        index = 0
        while True:
            token = os.getenv(f"GITHUB_API_TOKEN_{index}")
            if token is None:
                break
            tokens.append(token)
            index += 1
        return tokens
