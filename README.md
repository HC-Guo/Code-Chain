# Code-Chain
A Large-scale Repository-level Code Datasets for Continue Pre-training and Supervised Fine-tuning

## Dataset Card


## Download
You can directly download the Raw Codechain Dataset at URLs like this:

https://drive.google.com/file/d/1NJAHIf1KU1cSGra4COL0Q1CtTvx60sv2/view?usp=drive_link

The total size of the whole datasets is approximately 8.65GB.


## Dataset stats


|           Codechain                               |  | 
|-----------------------------------------------------|----------|
| Size                                       | 8.65GB    | 
| The Number of Chains| 562587 |
| The Number of Repos| 31182 |
| Average Chain Length| 1.79 |
| The Number of Chains (chain length > 1 )| 246776 |
| Average Chain Length (chain length > 1 )| 2.81 |


More details about these datasets and our processing steps can be found in our paper.



### Data Instances

Documents included in the file contain: codechains, a csv of index.
- `Codechains`: a series of txt files of concatenated python code of every chain.
- `index.csv`: the information mapping every chain to its code txt file for every repo. Each instance contains:
  * `filename`: a list contains the filenames of the concatenated code txt files.
  * `chains`: the specific dependency chains displayed in lists. 
            
Here's an example of the `index.csv`:
```
filename :[
‘../dataset/Codechains/CrossLoc_0_concatenated_files.txt',
’../dataset/Codechains/CrossLoc_1_concatenated_files.txt', '../dataset/Codechains/CrossLoc_2_concatenated_files.txt',
'../dataset/Codechains/CrossLoc_3_concatenated_files.txt', '../dataset/Codechains/CrossLoc_4_concatenated_files.txt',
'../dataset/Codechains/CrossLoc_5_concatenated_files.txt', ‘../dataset/Codechains/CrossLoc_6_concatenated_files.txt']

chains :[
	['CrossLoc/utils/learning.py', 'CrossLoc/loss/depth.py', ‘CrossLoc/finetune_decoder_single_task.py'],
  ['CrossLoc/dsacstar/setup.py'], 
	['CrossLoc/dataloader/__init__.py'], 
  ['CrossLoc/loss/semantics.py', 'CrossLoc/train_single_task.py'], 
	['CrossLoc/utils/learning.py', 'CrossLoc/train_single_task.py'], 
	['CrossLoc/dsacstar/setup_super.py'], 
	['CrossLoc/networks/networks.py', 'CrossLoc/utils/learning.py', ‘CrossLoc/test_single_task.py']
]

```
Each list in `chains` corresponds to a txt file. For a list [a.py, b.py, c.py]. The dependency relationship is : ‘a.py’ imported in ‘b.py’, ‘b.py’ imported in ‘c.py’. 

Here's an example text file of the `Codechains`, '....' means the original python code:

```
The code dependency chain is : ['Addarr/src/transmission.py', 'Addarr/src/addarr.py', 'Addarr/src/delete.py']
""" 
Addarr/src/transmission.py
"""

.......

""" 
Addarr/src/addarr.py
"""

.......

"""
'Addarr/src/delete.py'
"""

.......

```



## Licensing Information

[![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://lbesson.mit-license.org/)

This code is licensed under a MIT License.

[![CC BY-NC-SA 4.0](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg)](http://creativecommons.org/licenses/by-nc-sa/4.0/)

The benchmark is licensed under a
[Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-nc-sa/4.0/).



