from typing import List, Dict, Any
from gpt4_interface import get_gpt4_suggestions
from git2gpt.core import get_repo_snapshot, apply_gpt_mutations, commit_changes
import json


def extract_mutations(suggestions: str) -> List[Dict[str, Any]]:
    # Parse the JSON suggestions and extract the mutation objects
    return json.loads(suggestions)


def interact_with_gpt(snapshot: str) -> str:
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {
            "role": "user",
            "content": f"Here's the repo snapshot: {snapshot}. Suggest some changes.",
        },
    ]
    return get_gpt4_suggestions(messages)


if __name__ == "__main__":
    repo_path = "."  # Use the current directory as the repository path

    try:
        # 1. Provide a snapshot of the git repo in JSON to the GPT API
        snapshot = get_repo_snapshot(repo_path)
        suggestions = interact_with_gpt(snapshot)

        # 2. Process suggestions and extract mutations
        mutations = extract_mutations(suggestions)

        # 3. Mutate the repository as directed and commit the changes
        apply_gpt_mutations(repo_path, mutations)
        commit_changes(repo_path, "Applied GPT-4 suggested changes.")
    except Exception as e:
        print(f"An error occurred: {e}")
