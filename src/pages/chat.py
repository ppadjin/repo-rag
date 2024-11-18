import streamlit as st
from st_pages import get_pages, get_script_run_ctx 
from query_index import query_index
import time


def chat_page():
    st.set_page_config(page_title=st.session_state.last_repo, layout="wide")

    st.title("Chat with your repo")

    index = st.session_state.index

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("What is up?"):
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)
    # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

    response = ""

    if prompt:
        response = query_index(prompt, index=index)
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})



if 'last_repo' not in st.session_state.keys():
    st.write('No repository selected. Please select a repository to chat with.')

else:
    chat_page()