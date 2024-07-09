from utils.randomSelect import randomWalk
from utils.metric import calFrequency
from utils.concat import pyconcat
import json
import os
import pandas as pd
REPO_DIR =  "../Codechain/testrepo/"
GRAPH_DIR = "../Codechain/testgraph/"


 
if __name__ == "__main__":
    df = pd.DataFrame(columns=['filename', 'chains'])
    for filename in os.listdir(GRAPH_DIR):
        print(filename)
        with open(GRAPH_DIR + filename, 'r') as json_file:
            graph = json.load(json_file)  
        graphFrequency = calFrequency(graph)
        threshold = 100
        selected_chain = randomWalk(graph,graphFrequency,threshold) 
        txtName = pyconcat(selected_chain,REPO_DIR)
        new_row = {'filename': txtName, 'chains': selected_chain}
        df.loc[len(df)] = new_row
    
    df.to_csv("ndex.csv")
    print(df)
        