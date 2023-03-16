import argparse
import difflib
import json
import os
import sys

from typing import List, Dict, Any
from gpt4_interface import get_gpt4_suggestions
from git2gpt.core import (
    get_repo_snapshot,
    apply_gpt_mutations,
    commit_changes,
    get_file_diff,
)


def extract_mutations(suggestions: str) -> List[Dict[str, Any]]:
    return json.loads(suggestions)


def interact_with_gpt(snapshot: str) -> str:
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {
            "role": "user",
            "content": f"Here's the repo snapshot: {snapshot}. Suggest some changes in JSON format. Supported mutations are 'add', 'modify', and 'delete' for files, and 'delete' for empty directories only.",
        },
    ]
    return get_gpt4_suggestions(messages)


def display_diff(repo_path: str, mutations: List[Dict[str, Any]]) -> None:
    for mutation in mutations:
        file_path = mutation["file_path"]
        original_path = os.path.join(repo_path, file_path)
        original_content = ""
        if os.path.exists(original_path):
            with open(original_path, "r") as f:
                original_content = f.read()
        mutated_content = mutation.get("content", "")
        diff = list(
            difflib.unified_diff(
                original_content.splitlines(), mutated_content.splitlines()
            )
        )
        if diff:
            sys.stdout.writelines(line + "\n" for line in diff)


def main():
    parser = argparse.ArgumentParser(
        description="Modify a git repo using GPT-4 suggestions."
    )
    parser.add_argument(
        "prompt", type=str, help="User prompt for specific desired changes"
    )
    parser.add_argument(
        "--repo",
        default=".",
        help="Path to the git repository (default: current directory)",
    )
    parser.add_argument(
        "--no-diff",
        action="store_true",
        help="Disable showing the diff before committing changes",
    )
    args = parser.parse_args()

    repo_path = args.repo
    prompt = args.prompt
    show_diff = not args.no_diff

    try:
        snapshot = get_repo_snapshot(repo_path)
        suggestions = interact_with_gpt(snapshot, prompt)
        mutations = extract_mutations(suggestions)

        if show_diff:
            print("Proposed changes:")
            display_diff(repo_path, mutations)
            confirm = input("Do you want to apply these changes? [y/N]: ").lower()
            if confirm != "y":
                print("Aborted. No changes were applied.")
                sys.exit(0)

        apply_gpt_mutations(repo_path, mutations)
        commit_changes(repo_path, f"Applied GPT-4 suggested changes: {prompt}")

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
