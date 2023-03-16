import os
import subprocess
from typing import List, Dict, Any
from git2gpt.git_to_json import git_archive_to_json
import shutil
import difflib


def get_file_diff(original_content: str, mutated_content: str) -> List[str]:
    original_lines = original_content.splitlines()
    mutated_lines = mutated_content.splitlines()
    diff = list(difflib.unified_diff(original_lines, mutated_lines))
    return diff


def get_repo_snapshot(repo_path: str) -> str:
    return git_archive_to_json(repo_path)


def get_tracked_files(repo_path: str) -> List[str]:
    os.chdir(repo_path)
    result = subprocess.run(["git", "ls-files"], capture_output=True, text=True)
    tracked_files = result.stdout.splitlines()
    return tracked_files


def apply_gpt_mutations(repo_path: str, mutations: List[Dict[str, Any]]) -> None:
    os.chdir(repo_path)
    tracked_files = get_tracked_files(repo_path)

    for mutation in mutations:
        action = mutation["action"]
        file_path = mutation["file_path"]

        if file_path not in tracked_files:
            print(f"Skipping mutation for untracked file: {file_path}")
            continue

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
