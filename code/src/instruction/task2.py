import pandas as pd
import re
import json
import random
TXT_DIR = "../Codechain"
index = pd.read_csv("../Codechain/dataset/index.csv")

instruction = "Complete the corresponding code content based on the provided file contents and dependency relationships."

initial_json = []
count = 0 

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
                input_code = ""
                first_line = file.readline()
                input_code += first_line
                file_names = re.findall(r'\w+\.py', first_line)
                if len(file_names) > 4 or len(file_names) < 2:
                    continue
                file_names = [file_name[:-3] for file_name in file_names]
                output = ""
                for line in file:
                    if 'import' in line:
                        matches = re.findall(r'\b(?:{})\b'.format('|'.join(file_names)), line)
                        if matches:
                            start_position = random.randint(0, len(line))
                            modified_sentence = line[:start_position] + "#the content to be completed"
                            output += line 
                            
                        else:
                            input_code += line
                    else:
                        input_code += line 
            count += 1
            data = {
                    "instruction": instruction,
                    "input": input_code,
                    "output": output
                    }  
            print("Instruction No."+ str(count) + ":", sublist)
            initial_json.append(data)
    except Exception as e:
        with open("../Codechain/utils/instruction/error.txt", 'w') as error_file:
            error_file.write(f"Error occurred: {str(e)}\n")
            error_file.write("Traceback:\n")
            import traceback
            traceback.print_exc(file=error_file)                   
    
with open('../Codechain/dataset/instructions/instruction_task2.json', 'w') as outfile:
    json.dump(initial_json, outfile, indent=4)           
    

 
