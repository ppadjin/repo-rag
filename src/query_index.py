import os
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings, StorageContext
from llama_index.llms.groq import Groq
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.huggingface_api import HuggingFaceInferenceAPI
from transformers import AutoTokenizer
from llama_index.core import load_index_from_storage

def query_index(query_text:str, index:VectorStoreIndex=None, load_dir: str = None):
    """
    Query the index with a query string.

    query_text: str
        The query string to search for.
        
    index: VectorStoreIndex
        The index to query. If None, it will be loaded
        from the load_dir.
    load_dir: str
        Directory to load the index from. If index is not none, this is ignored
    """
    if index is None and load_dir is None:
        raise ValueError("Either index or load_dir must be provided.")
    
    if index is not None and load_dir is not None:
        load_dir = None
        raise Warning("Both index and load_dir are provided. index will be used.")
        
    groq_key = os.environ['GROQ_KEY']
    llm = Groq(model="llama3-70b-8192", api_key=groq_key)

    # Set up local embedding model
    embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-base-en-v1.5")

    Settings.llm = llm
    Settings.embed_model = embed_model
    
    if index is None:
        storage_context = StorageContext.from_defaults(persist_dir=load_dir)
        # load index
        index = load_index_from_storage(storage_context)

    query_engine = index.as_query_engine()

    response = query_engine.query(query_text)

    return response
