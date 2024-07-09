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
Write a configuration file for the project based on the following file contents and their dependency relationships. 
Give output following the example format
example:
"output": {
"configuration file": 
# Project configuration file
[dependencies]
Chatbot/chatbotconfig.py = [Chatbot/chatbot/__init__.py]
Chatbot/chatbot/__init__.py = [Chatbot/chatbot.py]
Chatbot/chatbot.py = []
# Other configuration items
[dependencies]
Chatbot/chatbotconfig.py = [os]
Chatbot/chatbot/__init__.py = [flask]
Chatbot/chatbot.py = []
"
}
'''

initial_json = []
count = 0 



if __name__ == "__main__":
    # test
    prompt_dic = {'system_prompt': "You are a helpful assistant."}
    for i in range(len(index)):
        item = index.loc[i,:]
        name = item["filename"]
        chain = item["chains"]
        paths_str = name

        paths_str = paths_str.strip('[]')
    
        paths_str = paths_str.replace("'", "")
   
        paths_list = paths_str.split(', ')
        try:
            for item in paths_list:
                path = item.replace("..",TXT_DIR)
                with open(path,'r') as file:
                    #input_code = instruction + content
                    first_line = file.readline()
                    input_code = first_line + file.read()
                    message = instruction + input_code
                    file_names = re.findall(r'\w+\.py', first_line)
                    if len(file_names) > 4 or len(file_names) < 2:
                        continue
                r = mit_spider_openai(
                model="gpt-4-1106-preview",
                messages=[
                    {"role": "system", "content": prompt_dic['system_prompt']},
                    {"role": "user", "content": message},
                ],
                # stop=["\n"],
                temperature=0.3,
            )
                response_message = r['data']['response']['choices'][0]['message']['content']
                count += 1
                data = {
                        "instruction": instruction,
                        "input": input_code,
                        "output": response_message
                        }  
                print("生成第"+ str(count) + "条指令:", first_line)
                initial_json.append(data)
        except Exception as e:
            with open("../Codechain/utils/instruction/error_task5.txt", 'w') as error_file:
                error_file.write(f"Error occurred: {str(e)}\n")
                error_file.write("Traceback:\n")
                import traceback
                traceback.print_exc(file=error_file)  

    with open('../Codechain/dataset/instructions/instruction_task5.json', 'w') as outfile:
        json.dump(initial_json, outfile, indent=4)   