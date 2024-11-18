import os
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.llms.groq import Groq
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.huggingface_api import HuggingFaceInferenceAPI
from transformers import AutoTokenizer

repo_dir = os.getcwd()

# Load documents
documents = SimpleDirectoryReader('data').load_data()

groq_key = os.environ['GROQ_KEY']
llm = Groq(model="llama3-70b-8192", api_key=groq_key)

# Set up local embedding model
embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-base-en-v1.5")

Settings.llm = llm
Settings.embed_model = embed_model

# Create index
index = VectorStoreIndex.from_documents(
    documents=documents,
    )

# Save index
save_dir = os.path.join(repo_dir, 'data', 'index')
index.storage_context.persist(save_dir)
