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

Documents are arranged as follows:

- `text_list`: a list of sentences comprising the text of the document
- `url`: the original url where the document was hosted
- `image_info` is a key mapping to a list of images. each image contains:
  - `image_name`: a filename that you could download the image to
  - `face_detections`: `None` if no faces are detected (which should be the case in "fewer faces")
  - `matched_text_index`: the index within `text_list` representing the sentence that this image is matched to
  - `matched_sim`: the CLIP ViT-L/14 similarity between the image and the sentence at the matched index
- `similarity_matrix`: a matrix of shape `len(image_info) x len(text_list)` where `similarity_matrix[i, j]` is the CLIP ViT-L/14 similarity between the `i`-th image and the `j`-th sentence.

Here's an example:

```

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
