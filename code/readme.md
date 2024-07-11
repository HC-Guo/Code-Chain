# Code for data curation
We open all the code used to collect and generate our data. You can use our process to generate more of the same data.
This repository contains scripts used for scraping and data generation purposes.
## File Overview
**code/src**: This is the code for Github data crawling and dependency graph generation.

**code/pyconcat**: This is the code for code-chain generaiton and concatenate the code into text files for each chain.

**code/instruction**: The code for generating instructions. The tasks of predicting dependencies from code and completing code based on dependencies are automated using scripts. The other three are completed with GPT4.

## code/src

### How to use

We use [Poetry](https://github.com/python-poetry/poetry) to manage the dependencies we need.
You can download the tool by:
```
pip install poetry
```

Make sure your python version >= 3.10

To run the program:
```
poetry install
poetry run python main.py
```


### Configuration

You need to fill in the following envrionment settings before you run the code. Save them in a `.env` file or directly fill them in the `config/setting.py`

```
R2_BUCKET_NAME =     #database settings, you can change them according to your own need.
R2_ENDPOINT =
R2_ACCESS_KEY =
R2_SECRET_KEY =
MONGODB_URL =
AZURE_CONN_STRING =
GITHUB_API_TOKEN_0 =   #personal fine-grained github tokens. The numbers depend on how many threads you need.
GITHUB_API_TOKEN_1 = 
```
### Documentaion

`main.py` : The functions `process_single_repo()` and `main()` are for single thread processing and multi threads processing seperately. You can choose different execution paths by commenting out different functions.

`utils/chain.py`: The scirpts we use to parser the syntax of the python code and generate dependency graphs for each repo.




