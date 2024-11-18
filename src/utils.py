import os
from typing import Callable



def list_files_with_condition(directory: str, condition: Callable[[str], bool]):
    """
    Recursively list all .sh files in a given directory
    
    Args:
        directory (str): Path to the directory to search
    
    Returns:
        list: Full paths of .sh files found
    """
    out_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if condition(file):
                out_files.append(os.path.join(root, file))
    return out_files

def list_sh_files(directory: str):
    """
    Recursively list all .sh files in a given directory
    
    Args:
        directory (str): Path to the directory to search
    
    Returns:
        list: Full paths of .sh files found
    """
    return list_files_with_condition(directory, lambda x: x.endswith('.sh'))

def list_md_files(directory: str):
    """
    Recursively list all .md files in a given directory
    
    Args:
        directory (str): Path to the directory to search
    
    Returns:
        list: Full paths of .md files found
    """
    return list_files_with_condition(directory, lambda x: x.endswith('.md'))


def get_relevant_files(repo_dir: str, include_md: bool = True, include_sh: bool = True):
    """
    Get relevant files from a repository directory
    
    Args:
        repo_dir (str): Path to the repository directory
        include_md (bool): Include markdown files
        include_sh (bool): Include shell script files
    
    Returns:
        set: Set of relevant files
    """
    relevant_files = set()
    if include_md:
        md_files = list_md_files(repo_dir)
        relevant_files.update(md_files)

    if include_sh:
        relevant_files.update(list_sh_files(repo_dir))
    return list(relevant_files)