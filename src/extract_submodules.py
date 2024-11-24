import os
from git import Repo
from utils import get_relevant_files


def extract_submodule_files(repo_path: str):
    """
    Extracts the relevant files from the submodules of a git repository
    """

    submodules_file_path = os.path.join(repo_path, '.gitmodules')

    # check if the .gitmodules file exists
    if not os.path.exists(submodules_file_path):
        return []

    submodules = []
    with open(submodules_file_path, 'r') as f:
        lines = f.readlines()

    for line in lines:
        if '.git' in line:
            submodules.append(line.split('=')[1].strip())

    # clone the submodules

    submodule_dir = os.path.join(repo_path, 'submodules')
    os.makedirs(submodule_dir, exist_ok=True)


    all_relevant_files = []
    for submodule in submodules:
        submodule_name = submodule.split('/')[-1]
        curr_submodule_dir = os.path.join(submodule_dir, submodule_name)
        if not os.path.exists(curr_submodule_dir):
            Repo.clone_from(submodule, curr_submodule_dir)

        curr_relevant_files = get_relevant_files(curr_submodule_dir)
        all_relevant_files.extend(curr_relevant_files)


    return all_relevant_files


