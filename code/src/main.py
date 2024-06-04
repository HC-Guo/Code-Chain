from app.services.multiple_process_service import process_multiple_repos
from app.services.service import RepoProcessor
from app.config import Settings
from app.utils.github_api import GithubAPI
def main():
    settings = Settings()

    # 设置线程数
    num_threads = 4 # 或者您可以根据需要修改这个值

    # 获取 GitHub API tokens
    tokens = settings.github_api_tokens

    # 检查是否有足够的 GitHub API tokens
    if len(tokens) < num_threads:
        print("Insufficient number of GitHub API tokens for the selected number of threads.")
        return

    # 执行多线程处理
    print('Starting multi-threaded processing...')
    process_multiple_repos(num_threads, tokens, 100)
    print('Processing completed successfully.')

def process_single_repo():
    settings = Settings()
    token = settings.github_api_tokens[3]
    github = GithubAPI(token)
    processor = RepoProcessor()
    processor.process_repos(github)

def test():
    settings = Settings()
    token = settings.github_api_tokens[3]
    github = GithubAPI(token)
    repos = github.search_repos("", "stars", "python", page=1, per_page=10)
    print(repos)
if __name__ == "__main__":
    #main()
    process_single_repo()
    #test()
