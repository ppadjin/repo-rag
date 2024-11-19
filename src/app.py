import os
import streamlit as st
import time
from git import Repo
from st_pages import get_pages, get_script_run_ctx 
from utils import get_relevant_files
from extract_submodules import extract_submodule_files

def load_github_files(repo_url):
    """
    Index the files in a GitHub repository
    """
    # check if the URL is valid
    # clone the repository
    repo_name = repo_url.split('/')[-1].replace('.git', '')
    repo_dir = 'data/' + repo_name
    if not os.path.exists(repo_dir):
        try:
            Repo.clone_from(repo_url, repo_dir)
        except:
            st.error('Invalid repository URL. Please try again.')
            return None

    # get the relevant files
    relevant_files = get_relevant_files(repo_dir)
    submodule_files = extract_submodule_files(repo_dir)
    relevant_files.extend(submodule_files)
    save_dir = 'index/' + repo_name
    # create the index
    index = create_index(input_files=relevant_files, save_dir=save_dir, model_provider='groq')

    return index



def main_page():
    st.set_page_config(page_title="Home", layout="wide")
    st.title('Github repo buddy')
    st.write('Setup the repo in minutes, not hours. Get all the help with installation and setup from buddy.')
    
    # app form
    with st.form('repo_form'):
        repo_url = st.text_input('Enter GitHub Repository URL')
        submit_button = st.form_submit_button('Setup Repository')
        
        if submit_button and repo_url:
            with st.spinner('Indexing repository files... This might take a few minutes...'):
                # Process the repository
                index = load_github_files(repo_url)
                if index is not None:
                    st.session_state.index = index
                    # repo name
                    repo_name = repo_url.split('/')[-1].replace('.git', '')
                    st.session_state.last_repo = repo_name
                    st.switch_page('pages/chat.py')


from create_index import create_index

# Initialize session state for page management
if 'page' not in st.session_state:
    st.session_state.page = 'app'
    

# Main page layout
query_params = st.query_params
page = query_params.get("page", ["app"])[0]

if page == 'app':
    main_page()
