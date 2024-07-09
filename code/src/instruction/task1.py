import pandas as pd
import re
import json
REPO_DIR = "../Codechain/repos/code_chain/"
index = pd.read_csv("../Codechain/dataset/index.csv")


instruction = "Analyze the following code snippet to determine the dependency relationship between files."

initial_json = []
count = 0 
for i in range(len(index)):
    item = index.loc[i,:]
    chain = item["chains"]
    sublists = re.findall(r'\[([^[\]]*)\]', chain)
    elements = [re.split(r',\s*', sublist) for sublist in sublists]
    for sublist in elements:
        if len(sublist) >= 2 and len(sublist) <= 4:
            for file in sublist:
                path = REPO_DIR + file.strip("'")
                pyname = file.strip("'")
                file_contents = ""
                with open(path, 'r') as file:
                    content = file.read()
                    file_contents += '""" \n' + pyname + '\n"""' + "\n" + content + "\n\n"
                    #print(content)
            count += 1
            input_code = file_contents
            output_files = sublist
            data = {
                    "instruction": instruction,
                    "input": input_code,
                    "output": output_files
                    }
            print("Instruction No."+ str(count) + ":", sublist)
            initial_json.append(data)

            
with open('../Codechain/dataset/instructions/instruction_task1.json', 'w') as outfile:
    json.dump(initial_json, outfile, indent=4)           
    
