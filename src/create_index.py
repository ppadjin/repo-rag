import os
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.llms.groq import Groq
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import load_index_from_storage, StorageContext
from llama_index.llms.huggingface_api import HuggingFaceInferenceAPI
from transformers import AutoTokenizer
from typing import List

def create_index(input_dir: str = None, input_files: List[str] = None, save_dir='index', model_provider='groq'):
    """
    Create an index from a directory or a list of files. Saves the index for later.

    input_dir: str
        Directory containing the documents to be indexed.
    input_files: List[str]
        List of files to be indexed. If input_files is provided, input_dir is ignored.
    save_dir: str
        Directory to save the index.
    """
    llm = None
    if model_provider == 'groq':
        groq_key = os.environ['GROQ_KEY']
        llm = Groq(model="llama3-70b-8192", api_key=groq_key)


    # Set up local embedding model
    embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-base-en-v1.5")

    Settings.llm = llm
    Settings.embed_model = embed_model

    if os.path.exists(save_dir) and os.path.exists(os.path.join(save_dir, "index_store.json")):
        print('Index already exists. Loading...')

        storage_context = StorageContext.from_defaults(persist_dir=save_dir)
        index = load_index_from_storage(storage_context)
        return index

    if not input_dir and not input_files:
        raise ValueError("Either input_dir or input_files must be provided.")
    
    if input_dir and input_files:
        input_dir = None
        raise Warning("Both input_dir and input_files are provided. input_files will be used.")

    # Load documents
    documents = SimpleDirectoryReader(input_dir=input_dir, input_files=input_files).load_data()

    # Create index
    index = VectorStoreIndex.from_documents(
        documents=documents,
        )

    # Save index
    index.storage_context.persist(save_dir)
    return index
