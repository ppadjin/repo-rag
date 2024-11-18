import os
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.llms.groq import Groq
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.huggingface_api import HuggingFaceInferenceAPI
from transformers import AutoTokenizer
from typing import List
from git import Repo  # pip install gitpython


from src.create_index import create_index
from src.query_index import query_index
from src.utils import list_md_files, list_sh_files, get_relevant_files


git_url = "https://github.com/coltonstearns/dynamic-gaussian-marbles.git"
# extract the repo name from the git url
repo_name = git_url.split("/")[-1].replace(".git", "")

# clone this repo in data folder
repo_dir = os.path.join("data", repo_name)
if not os.path.exists(repo_dir):
    Repo.clone_from(git_url, repo_dir)

include_md = True
include_sh = True

relevant_files = get_relevant_files(repo_dir, include_md=include_md, include_sh=include_sh)


index_dir = os.path.join("index", repo_name)
relevant_files = list(relevant_files)
index = create_index(input_files=relevant_files, save_dir=index_dir, model_provider='groq')

# query the index
query_text = "Give me steps to run the training pipeline. Where should I run the preprocessing script from (which subdir)?"
response = query_index(query_text, index=index)

print(response)