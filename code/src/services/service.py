import threading
import queue
import logging


from app.utils import GithubAPI, chain
from app.db import AzureBlobStorage, MongoDB, CloudflareR2

log_input_handler = logging.FileHandler('process_output.log')
log_input_handler.setLevel(logging.INFO)

log_input_logger = logging.getLogger('inputLogger')
log_input_logger.setLevel(logging.INFO)
log_input_logger.addHandler(log_input_handler)


class RepoProcessor:
    def __init__(self):
        self.mongodb = MongoDB()
        self.r2 = CloudflareR2()
        self.azure = AzureBlobStorage()
        self.last_star = self.mongodb.load_last_star()

    def process_repos(self, github):
        print("Processing repos...")
        repos = github.search_repos("", "stars", "python", self.last_star, page=1, per_page=1000)
        print("repos has been searched")
        
        for repo in repos:
            try:
                repo_info = github.fetch_repository(repo['owner']['login'], repo['name'])
                print(f"repo info has been fetched: {repo_info}")
                files = github.extract_files(repo['owner']['login'], repo['name'], '')
                print("repos search has been done")

                file_keys = []
                for file in files:
                    key = self.azure.save(file['path'], file['content'], repo['name'])
                    file_keys.append(key)
                print("files has been saved")
                log_input_logger.info(f"{repo['name']} repo has been upload to cloud and file keys is: {file_keys}")
                
                repo_name = repo['name']
                chain_generator = chain(self.azure, file_keys)
                graph_key = chain_generator.generate(repo_name)
                print("Dependency graph has been generated and saved")
                log_input_logger.info(f"{repo['name']} repo has been proceesed and the graphy file is: {graph_key}")
                

                document = {
                    "repo_info": repo_info,
                    "file_keys": file_keys,
                    "last_star": repo['stargazers_count'],
                    "   ": graph_key
                }   
                self.mongodb.save(document)
                print("document has been saved")
            

                self.last_star = repo['stargazers_count']
                print(f"last_star: {self.last_star} has been saved")
                self.mongodb.save_last_star(self.last_star)
            except Exception as exc:
                print(f"Error processing repo {repo['name']}: {exc}")
    def process_in_thread(self, task_queue):
        while True:
            github = task_queue.get()  
            if github is None:
                break  
            self.process_repos(github) 
            task_queue.task_done()  

def process_multiple_repos(num_threads, tokens):
    task_queue = queue.Queue()
    threads = []


    assert len(tokens) >= num_threads, "Token数量少于线程数量"


    for i in range(num_threads):
        token = tokens[i % len(tokens)]  
        github_api = GithubAPI(token)   
        task_queue.put(github_api)       

        processor = RepoProcessor()      
        thread = threading.Thread(target=processor.process_in_thread, args=(task_queue,))
        thread.start()
        threads.append(thread)

    for _ in range(num_threads):
        task_queue.put(None)


    for thread in threads:
        thread.join()