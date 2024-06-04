import requests
import base64
import os
import time
import random
import concurrent.futures

# from app.config import Settings
# setting = Settings()
# tokens = setting.github_api_tokens

class GithubAPI:

    BASE_URL = "https://api.github.com"

    def __init__(self, token):
        self.headers = {"Authorization": "Bearer " + token}

    def search_repos(self, query: str, sort: str, language: str, last_star: int = None, page: int = 1, per_page: int = 100):
        url = f"{self.BASE_URL}/search/repositories"

        # 添加star数，archived状态，fork状态等条件
        full_query = f"{query} language:{language} archived:false fork:false"
        if last_star is not None:
            # 添加star数条件
            full_query += f" stars:<{last_star}"

        params = {"q": full_query, "sort": sort, "page": page, "per_page": per_page}

        response = requests.get(url, headers=self.headers, params=params)

        if response.status_code != 200:
            raise Exception(f"Request failed: {response.status_code}")

        return response.json()['items']

    def fetch_repository(self, owner, repo):
        url = f"{self.BASE_URL}/repos/{owner}/{repo}"

        response = requests.get(url, headers=self.headers)

        if response.status_code != 200:
            raise Exception(f"Request failed: {response.status_code}")

        return response.json()

    def list_contents(self, owner, repo, path):
        for _ in range(5):  # Retry up to 5 times
            response = requests.get(
                f"https://api.github.com/repos/{owner}/{repo}/contents/{path}",
                headers=self.headers
            )
            if response.status_code == 200:
                return response.json()

            print(f"Request failed with {response.status_code}, retrying...")
            time.sleep(5)  # Wait for a bit before retrying

        # If we've retried 5 times and still failed, give up
        response.raise_for_status()

    def extract_files(self, owner, repo, path='', local_dir=''):
        contents = self.list_contents(owner, repo, path)
        files = []

        for item in contents:
            # 处理文件类型的内容
            if item['type'] == 'file' and item['name'].endswith('.py'):
                try:
                    file_content = self.fetch_file_content(item['git_url'])
                    files.append({
                        'path': os.path.join(local_dir, item['name']),
                        'content': file_content
                    })
                except Exception as exc:
                    raise Exception(f"Error fetching file content: {exc}")

            # 递归处理目录类型的内容
            elif item['type'] == 'dir':
                try:
                    files.extend(self.extract_files(owner, repo, item['path'], os.path.join(local_dir, item['name'])))
                except Exception as exc:
                    raise Exception(f"Error processing directory: {exc}")

        return files

    def fetch_file_content(self, url):
        response = requests.get(url, headers=self.headers)

        if response.status_code != 200:
            raise Exception(f"Request failed: {response.status_code}")

        content = response.json()['content']
        decoded_content = base64.b64decode(content).decode()

        return decoded_content     
