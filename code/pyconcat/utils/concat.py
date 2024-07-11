import pandas as pd
import re

def pyconcat(selected_chain, REPO_DIR):
    file_paths = []
    count = 0
    result_list = []

    # Read files one by one and concatenate contents
    for chain in selected_chain:
        concatenated_content = ""
        strings = chain[0].split('/')

        reponame = strings[0]
        for file_path in chain:
            file_path = REPO_DIR + file_path
            with open(file_path, "r") as file:
                concatenated_content += file.read() + "\n\n"
        
        txt_name = "../Codechain/testrepo/testchains/" + reponame +"_"+ str(count) + "_concatenated_files.txt"
        
        with open(txt_name, "w") as output_file:
            output_file.write(concatenated_content)
        
        result_list.append(txt_name)
        count += 1

    return result_list

