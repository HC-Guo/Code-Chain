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
Generate a README document for the project based on the following file contents and dependency relationships. 
Give output following the example format
example:
"output":{
"README.md":
#ProjectOverview
##FileDependencyRelationships
-`chatbotconfig.py`dependson`chatbot/chatbot/__init__.py`
-`chatbot/chatbot/__init__.py`dependson`chatbot/chatbot.py`
##FileDescriptions
-`chatbot/chatbotconfig.py`:Contains configuration settings for the chatbot.
-`chatbot/chatbot/__init__.py`:Initializes the chat bot application and loads necessary
dependencies such as Flask,Keras,NLTK,andtrainedmodels.
-`chatbot/chatbot.py`:Entry point for the chat bot application.
}
'''

prompt= "Generate a README document for the project based on the following file contents and dependency relationships. "


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
        # 去除开头和结尾的方括号
        paths_str = paths_str.strip('[]')
        # 去除每个路径项外的单引号
        paths_str = paths_str.replace("'", "")
        # 使用 split() 方法按照逗号加空格分割字符串
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
                    with open('../Codechain/dataset/instructions/instruction_task3.json', 'r') as file:
                        initial_json = json.load(file)
                    with open('../Codechain/dataset/instructions/instruction_task3.json', 'w') as outfile:
                        initial_json.append(result)
                        json.dump(initial_json, outfile)
                        print(f"生成第 {count} 条指令:", result['input'].split('\n', 1)[0])
            except Exception as exc:
                with open("/data/hongcheng_guo/JJ/Codechain/utils/instruction/error_task3.txt", 'a') as error_file:
                    error_file.write(f'处理时出现异常: {exc}\n')
                    error_file.write(f"Error occurred: {str(exc)}\n")
                    error_file.write("Traceback:\n")
                    import traceback
                    traceback.print_exc(file=error_file)   
   

