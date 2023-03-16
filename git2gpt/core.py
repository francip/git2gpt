import os
import subprocess
from typing import List, Dict, Any
from git2gpt.git_to_json import git_archive_to_json


def get_repo_snapshot(repo_path: str) -> str:
    return git_archive_to_json(repo_path)


def apply_gpt_mutations(repo_path: str, mutations: List[Dict[str, Any]]) -> None:
    os.chdir(repo_path)
    for mutation in mutations:
        action = mutation["action"]
        file_path = mutation["file_path"]
        if action == "add":
            with open(file_path, "w") as f:
                f.write(mutation["content"])
        elif action == "modify":
            with open(file_path, "w") as f:
                f.write(mutation["content"])
        elif action == "delete":
            if os.path.isfile(file_path):
                os.remove(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)


def commit_changes(repo_path: str, commit_message: str) -> None:
    os.chdir(repo_path)
    subprocess.run(["git", "add", "."])
    subprocess.run(["git", "commit", "-m", commit_message])
