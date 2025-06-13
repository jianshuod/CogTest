## Towards Understanding the Cognitive Habits of Large Reasoning Models

This repository includes codes for prompting LLMs for task construction and evaluating cognitive habits of Large Reasoning Models.


### Preparations

1. Before running the scripts, you should first configue your API keys in the `.env` file.

2. You are advised to install the suitable libraries according to
```shell
conda env create -f environment.yaml
```

### Codebase Structure
```
- assets
    - instructions: the final version of tasks used in the paper
- src
    - llm.py: unified interfaces for querying LRMs through API
    - tools.py: mainly the code for habit extraction
- .env: configuration file
- main.ipynb: codes for eliciting CoTs and extracting cognitive habits
- task-construction.ipynb: principles and codes for generating tasks for the 10 non-reasoning habits
```

### Get Started
For replication of cognitive habit evaluation, you can just rush to the `main.ipynb`.

If you are interested in supporting more models, please kindly add necessary implementations for querying the corresponding LLM APIs (e.g., OpenAI or vLLM) and parsing CoTs.