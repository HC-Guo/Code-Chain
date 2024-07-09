import os
import time
import requests
import pandas as pd
import pandas as pd
import re
import json
import random
import concurrent.futures


# set environment variable
os.environ["MIT_SPIDER_TOKEN"] = ""  #gpt token
os.environ["M6_TENANT"] = ""
os.environ["MIT_SPIDER_URL"] = ""

MAX_API_RETRY = 3
LLM_MIT_RETRY_SLEEP = 5

def mit_spider_openai(**kwargs):
    if not os.environ.get('MIT_SPIDER_TOKEN', None):
        print("NO MIT_SPIDER_TOKEN FOUND，please set export MIT_SPIDER_TOKEN=<YOUR TOKEN>")
    if not os.environ.get('MIT_SPIDER_URL', None):
        print("NO MIT_SPIDER_URL FOUND，please set export MIT_SPIDER_URL=<YOUR URL>")
    mit_spider_config = {
        "url": os.environ.get("MIT_SPIDER_URL", None),
        "header": {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {os.environ.get('MIT_SPIDER_TOKEN', None)}"
        }
    }
    tenant = None
    if kwargs['model'].startswith('gpt-4') and os.environ.get("M6_TENANT", None):
        tenant = os.environ.get("M6_TENANT")
    response = None
    for i in range(MAX_API_RETRY):
        try:
            if tenant:
                payload = {'tenant': tenant}
            else:
                payload = dict()
            for k, w in kwargs.items():
                payload[f"{k}"] = w
            response = requests.post(mit_spider_config['url'], json=payload, headers=mit_spider_config['header']).json()
        except Exception as e:
            print(response, e)
            time.sleep(LLM_MIT_RETRY_SLEEP)
            continue
        if response['code'] == 200:
            return response
        else:
            time.sleep(LLM_MIT_RETRY_SLEEP)
            print(response)
    return None


TXT_DIR = "../Codechain".  #your path for codechain txt files
index = pd.read_csv("../dataset/index.csv")

instruction = '''
Generate interface documentation based on the following code file contents. 
Give output following the example format
example:
"output":{
"Interface Documentation": 
# Interface Documentation
## File: chatbot/__init__.py
### Dependencies:
- `Flask`: Web framework for creating the chatbot application.
- `chatbotconfig.Config`: Configuration settings imported from `chatbotconfig.py`.
### Loaded Dependencies:
- `keras`: Deep learning library for building and training models.
- `nltk`: Natural Language Toolkit for natural language processing tasks.
- `pickle`: Python module for serializing and deserializing objects.
### Variables:
- `app`: Flask application instance.
- `model`: Loaded Keras model for the chatbot.
### Routes:
- `routes`: Module containing routes for the chatbot application.
---
## File: chatbot.py
### Dependencies:
- `app`: Flask application instance imported from the `chatbot` package.

}

'''

prompt= "Generate interface documentation based on the following code file contents.  "


initial_json = []
count = 0 

def process_item(item, instruction, prompt_dic):
    path = item.replace("..", TXT_DIR)

    with open(path, 'r') as file:
        first_line = file.readline()
        input_code = first_line + file.read()
        message = instruction + input_code
        file_names = re.findall(r'\w+\.py', first_line)
        if len(file_names) > 4 or len(file_names) < 2:
            return None

    r = mit_spider_openai(
        model="gpt-4-1106-preview",
        messages=[
            {"role": "system", "content": prompt_dic['system_prompt']},
            {"role": "user", "content": message},
        ],
        temperature=0.3,
    )
    
    response_message = r['data']['response']['choices'][0]['message']['content']
    
    data = {
        "instruction": prompt,
        "input": input_code,
        "output": response_message
    }
    return data



if __name__ == "__main__":
    # test
    prompt_dic = {'system_prompt': "You are a helpful assistant."}
    path_list = []
    for i in range(len(index)):
        item = index.loc[i,:]
        name = item["filename"]
        chain = item["chains"]
        paths_str = name
  
        paths_str = paths_str.strip('[]')

        paths_str = paths_str.replace("'", "")

        paths_list = paths_str.split(', ')
        path_list.extend(paths_list)

    with concurrent.futures.ThreadPoolExecutor(max_workers = 16) as executor:
        futures = []
        for item in path_list:
            future = executor.submit(process_item, item, instruction, prompt_dic)
            futures.append(future)

# 收集结果
        
        for future in concurrent.futures.as_completed(futures):
            try: 
                result = future.result()
                if result is not None:
                    count+=1
                    with open('../Codechain/dataset/instructions/instruction_task4.json', 'r') as file:
                        initial_json = json.load(file)
                    with open('../Codechain/dataset/instructions/instruction_task4.json', 'w') as outfile:
                        initial_json.append(result)
                        json.dump(initial_json, outfile)
                        print(f"生成第 {count} 条指令:", result['input'].split('\n', 1)[0])
            except Exception as exc:
                with open("../Codechain/utils/instruction/error_task4.txt", 'a') as error_file:
                    error_file.write(f"Error occurred: {str(exc)}\n")
                    error_file.write("Traceback:\n")
                    import traceback
                    traceback.print_exc(file=error_file)   
   