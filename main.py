import argparse
import difflib
import json
import os
import sys

from typing import List, Dict, Any
from gpt4_interface import get_gpt4_suggestions
from git2gpt.core import (
    apply_gpt_mutations,
    get_repo_snapshot,
    get_file_diff,
)


def extract_mutations(suggestions: str) -> List[Dict[str, Any]]:
    if suggestions.startswith("```"):
        suggestions = suggestions[8:-3] # strip the "```json\n" and "```"
    try:
        mutations = json.loads(suggestions)
    except json.JSONDecodeError as e:
        print(f"Failed to parse JSON: {e}")
        print(f"Invalid suggestions: {suggestions}")
        raise
    return mutations


def interact_with_gpt(snapshot: str, ask_question: bool, prompt: str) -> str:
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
    ]
    if ask_question:
        messages.append(
            {
                "role": "user",
                "content": f"Answer the following question about the code: {prompt}",
            }
        )
    else:
        messages.append(
            {
                "role": "user",
                "content": f"Update the repostiory with the following changes: {prompt}",
            }
        )
    return get_gpt4_suggestions(messages)


def main():
    parser = argparse.ArgumentParser(
        description="Modify a git repo using GPT-4 suggestions."
    )
    parser.add_argument(
        "prompt", type=str, help="User prompt for specific desired changes or question"
    )
    parser.add_argument(
        "--repo",
        default=".",
        help="Path to the git repository (default: current directory)",
    )
    parser.add_argument(
        "--ask",
        action="store_true",
        help="Enable ask mode to ask questions about the code instead of modifying it",
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
    ask_question = args.ask

    try:
        snapshot = get_repo_snapshot(repo_path)
        suggestions = interact_with_gpt(snapshot, ask_question, prompt)
        if ask_question:
            print(suggestions)
        else:
            mutations = extract_mutations(suggestions)

            if show_diff:
                print("Proposed changes:")
                display_diff(repo_path, mutations)
                confirm = input("Do you want to apply these changes? [y/N]: ").lower()
                if confirm != "y":
                    print("Aborted. No changes were applied.")
                    sys.exit(0)

            apply_gpt_mutations(repo_path, mutations)
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
