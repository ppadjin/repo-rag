import os
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings, StorageContext
from llama_index.llms.groq import Groq
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.huggingface_api import HuggingFaceInferenceAPI
from transformers import AutoTokenizer
from llama_index.core import load_index_from_storage


repo_dir = os.getcwd()

load_dir = os.path.join(repo_dir, 'data', 'index')

groq_key = os.environ['GROQ_KEY']
llm = Groq(model="llama3-70b-8192", api_key=groq_key)

# Set up local embedding model
embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-base-en-v1.5")

Settings.llm = llm
Settings.embed_model = embed_model

storage_context = StorageContext.from_defaults(persist_dir=load_dir)
# load index
index = load_index_from_storage(storage_context)

query_engine = index.as_query_engine()

response = query_engine.query("What does Romeo think about Juliet")

print(response)