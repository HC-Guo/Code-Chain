# Dataset Card for CodeChain

## Table of Contents
- [Dataset Description](#dataset-description)
  - [Dataset Summary](#dataset-summary)
  - [Supported Tasks](#supported-tasks-and-leaderboards)
  - [Code Languages](#languages)
- [Dataset Structure](#dataset-structure)
  - [Data Instances](#data-instances)
  - [Data Fields](#data-fields)
  - [Data Splits](#data-splits)
- [Dataset Creation](#dataset-creation)
  - [Curation Rationale](#curation-rationale)
  - [Source Data](#source-data)
  - [Annotations](#annotations)
  - [Personal and Sensitive Information](#personal-and-sensitive-information)
- [Considerations for Using the Data](#considerations-for-using-the-data)
  - [Social Impact of Dataset](#social-impact-of-dataset)
  - [Discussion of Biases](#discussion-of-biases)
  - [Other Known Limitations](#other-known-limitations)
- [Additional Information](#additional-information)
  - [Dataset Curators](#dataset-curators)
  - [Licensing Information](#licensing-information)
  - [Citation Information](#citation-information)

## Dataset Description

- **Homepage:** www.github.com/allenai/mmc4
- **Repository:** www.github.com/allenai/mmc4
- **Paper:** https://arxiv.org/abs/2304.06939
- **Point of Contact:** Jack Hessel (jackh@allenai.org)

### Dataset Summary

We release [CodeChain](https://www.tensorflow.org/datasets/catalog/c4), a large-scale repository-level code datasets for finetuing. We collecte over 50,000 Python repositories from GitHub, extract dependency relationships between files in each repository, and compile this information into dependency graphs saved as json files. After filtering out repositories with no dependency relationship and constructing chains using our random walk algorithm, CodeChain contains 562587 chains from 31182 repositories. A text file is concatenated for each chain, with the Python code arranged in the sequence of their import calls according to the dependency chain.

### Supported Tasks and Leaderboards

This is a pre-training corpus.

### Code Languages
Python

## Dataset Structure


### Dataset stats

|           Codechain                               |  | 
|-----------------------------------------------------|----------|
| Size                                       | 8.65GB    | 
| The Number of Chains| 562587 |
| The Number of Repos| 31182 |
| Average Chain Length| 1.79 |
| The Number of Chains (chain length > 1 )| 246776 |
| Average Chain Length (chain length > 1 )| 2.81 |


More details about these datasets and our processing steps can be found in our paper xxxxx



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


### Data Fields

See above.

### Data Splits

N/A, this is a pretraining corpus.

## Dataset Creation

The dataset was created from the middle of 2024 to early 2023 at the Allen Institute for AI.

### Curation Rationale

In-context learning \cite{brown2020language} enables sequence models to adapt to new tasks without any parameter updates by interleaving a few supervised examples in a prompt. 

### Source Data

#### Initial Data Collection and Normalization

See the paper for more details.

#### Who are the source language producers?

Authors of publicly accessible webpages.

### Annotations

#### Annotation process

See the paper for more details. The corpus, as a whole, is not explicitly annotated.

#### Who are the annotators?

N/A

### Personal and Sensitive Information

See the paper for an assessment of the risks of releasing image URLs. In particular, for the public, directly-downloadable corpus, we attempt to remove instances with faces.

## Considerations for Using the Data

### Social Impact of Dataset

Potential benefits:

- Useful as a pretraining corpus for in-context vision+language models; such models could be adapted later to better align with human preferences/express fewer pernicious social biases
- As in-context vision+language models become more common, if the standard pretraining set is public, it will be easier to audit models with respect to the training corpora.

Potential risks:

- As with most large-scale image datasets: images of individuals who did not explicitly consent to be in the dataset are included. Given the scale of the dataset, we think the risk of including these images is similar to the risk of such images being indexed by search engines.
- mmc4 inherits the risks of the text-only version of c4, e.g., the internet reflects pernicious social biases, and thus models trained on this corpus might also reproduce those biases at test time.

### Discussion of Biases

Web data, especially taken as a whole, often reflects the biases present in society. We encourage model trainers to reflect upon the distinction between an observational model of web text (e.g., as a means of auditing what is contained in that web text) versus a model that one endorses the outputs of as "correct", vs. one connects to other downstream systems that cause deployed systems to make decisions.

### Other Known Limitations

- The dataset is English only.
- Our filtration process discards images that do not relate to the text of web-pages above a specific model-estimated threshold. This might erase images/webpages that use image content in more creative, non-iteral ways.

## Additional Information

### Dataset Curators

This dataset was initially curated by researchers from AI2, UCSB, University of Washington, Columbia University, Yonsei University. The author list of v1 of the arxiv paper is an accurate list of specific contributors.

### Licensing Information

- The new contributions of mmc4 are released under ODC-BY.
- By using mmc4, be aware of that you are also bound by the Common Crawl terms of use.

### Citation Information

```
```
