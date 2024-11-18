import git
import os
import streamlit as st
import time
from st_pages import get_pages, get_script_run_ctx 
from ..src.create_index import create_index
from ..src.utils import get_relevant_files

def load_github_files(repo_url):
    """
    Index the files in a GitHub repository
    """
    # check if the URL is valid
    try:
        repo = git.Repo(repo_url)
        # clone the repository
        repo_name = repo_url.split('/')[-1].replace('.git', '')
        repo_dir = 'data/' + repo_name
        if not os.path.exists(repo_dir):
            git.Repo.clone_from(repo_url, repo_dir)
        
        # get the relevant files
        relevant_files = get_relevant_files(repo_dir)
        save_dir = 'index/' + repo_name
        # create the index
        index = create_index(input_files=relevant_files, save_dir=save_dir, model_provider='groq')

        return index
    except:
        st.write('Invalid GitHub repository URL. Please try again.')
        return None


def main_page():
    st.title('GitHub Repository Analyzer')
    
    # app form
    with st.form('repo_form'):
        repo_url = st.text_input('Enter GitHub Repository URL')
        submit_button = st.form_submit_button('Analyze Repository')
        
        if submit_button and repo_url:
            with st.spinner('Loading repository files... Please wait...'):
                # Process the repository
                index = load_github_files(repo_url)
                if index is not None:
                    st.session_state.index = index
                    switch_to_chat()


# Initialize session state for page management
if 'page' not in st.session_state:
    st.session_state.page = 'app'

def switch_to_chat():
    
    st.switch_page('pages/chat.py')

# Main page layout
query_params = st.query_params
page = query_params.get("page", ["app"])[0]

if page == 'app':
    main_page()
