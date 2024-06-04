import threading
import queue
import logging

from app.utils import GithubAPI, chain
from app.db import AzureBlobStorage, MongoDB, CloudflareR2


class RepoProcessor:
    def __init__(self, github):
        self.github = github
        self.mongodb = MongoDB()
        self.r2 = CloudflareR2()
        self.azure = AzureBlobStorage()
        self.last_star = self.mongodb.load_last_star()

    def process_repo(self, repo):
        repo_name = repo['name']

        try:
            repo_info = self.github.fetch_repository(repo['owner']['login'], repo_name)
            files = self.github.extract_files(repo['owner']['login'], repo_name, '')

            file_keys = []
            for file in files:
                key = self.azure.save(file['path'], file['content'], repo_name)
                file_keys.append(key)

            chain_generator = chain(self.azure, file_keys)  
            graph_key = chain_generator.generate(repo_name)

            document = {
                "repo_info": repo_info,
                "file_keys": file_keys,
                "last_star": repo['stargazers_count'],
                "graph_key": graph_key
            }
            self.mongodb.save(document)

            self.last_star = repo['stargazers_count']
            self.mongodb.save_last_star(self.last_star)

        except Exception as exc:
            print(f"Error processing repo {repo_name}: {exc}")

    def process_in_thread(self, task_queue):
        while True:
            repo = task_queue.get()
            if repo is None:
                break
            self.process_repo(repo)
            task_queue.task_done()


def generate_tasks(github, last_star):
    """ 生成任务列表 """
    repos = github.search_repos("", "stars", "python", last_star, page=1, per_page=1000)
    return repos

def process_multiple_repos(num_threads, tokens, repeat_times=5):
    for _ in range(repeat_times):
        task_queue = queue.Queue()
        threads = []

        main_github_api = GithubAPI(tokens[0])
        last_star = MongoDB().load_last_star()
        repos = generate_tasks(main_github_api, last_star)

        for repo in repos:
            task_queue.put(repo)

        for i in range(num_threads):
            token = tokens[i % len(tokens)]
            github_api = GithubAPI(token)
            processor = RepoProcessor(github_api)
            thread = threading.Thread(target=processor.process_in_thread, args=(task_queue,))
            thread.start()
            threads.append(thread)

        for _ in range(num_threads):
            task_queue.put(None)

        for thread in threads:
            thread.join()

        print(f"Processing batch {_+1} completed.")
