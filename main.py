import argparse
import difflib
import json
import os
import sys
from typing import List, Dict, Any
from gpt4_interface import get_gpt4_suggestions
from git2gpt.core import apply_gpt_mutations, get_repo_snapshot, get_file_diff, get_tracked_files, commit_changes


def extract_mutations(suggestions: str) -> List[Dict[str, Any]]:
    if suggestions.startswith("```"):
        suggestions = suggestions[8:-3] # strip the "```json\n" and "```"
    try:
        mutations = json.loads(suggestions)
    except json.JSONDecodeError as e:
        print(f"Failed to parse JSON: {e}")
        tempfile = 'error_log.json'
        with open(tempfile, 'w') as f:
            f.write(suggestions)
        print(f'Invalid suggestions saved to {tempfile} for debugging.')
        raise
    return mutations


def interact_with_gpt(snapshot: str, prompt: str, question: bool = False) -> str:
    messages = [
        {
            "role": "system",
            "content": f"You are an impressive and thorough software development assistant. You reply only in JSON. Here is a snapshot of a repository: {snapshot}",
        },
        {
            "role": "system",
            "content": """Respond to the user's request with a list of mutations to apply to the repository, using the following JSON format.

Each mutation in the list must include an action, a file_path, and a content (for insert and update operations). The action can be one of the following strings: 'add', 'modify', 'delete'.
It is extremely important that you do not reply in any way but with an exact JSON string. Do not supply markup or any explanations outside of the code itself.
""",
        },
        {
            "role": "user",
            "content": f"Update the repostiory with the following changes: {prompt}" if not question else f"Ask a question about the code: {prompt}"
        },
    ]
    return get_gpt4_suggestions(messages)


def display_diff(repo_path: str) -> None:
    tracked_files = get_tracked_files(repo_path)
    os.chdir(repo_path)
    for file in tracked_files:
        os.system(f'git diff --staged -- {file}')


def main():
    parser = argparse.ArgumentParser(
        description="Modify a git repo using GPT-4 suggestions or ask a question about the code."
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
        "--ask",
        action="store_true",
        help="Ask a question about the code, rather than modify it",
    )
    args = parser.parse_args()

    repo_path = args.repo
    prompt = args.prompt
    ask_question = args.ask

    try:
        snapshot = get_repo_snapshot(repo_path)
        suggestions = interact_with_gpt(snapshot, prompt, question=ask_question)

        if ask_question:
            print(f'Answer: {suggestions}')
        else:
            mutations = extract_mutations(suggestions)
            apply_gpt_mutations(repo_path, mutations)
            display_diff(repo_path)
            decision = input("Do you want to keep the changes? (y/n): ")
            if decision.lower() == 'y':
                commit_changes(repo_path, f"Applied changes from prompt: {prompt}")
            else:
                print("No changes will be committed.")
                print("To discard the changes, run the following git command:")
                print("    git reset --hard HEAD")

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
