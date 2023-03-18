import argparse
import sys

from gpt4_interface import get_gpt4_suggestions
from git2gpt.core import get_repo_snapshot


def interact_with_gpt(snapshot: str, question: str) -> str:
    messages = [
        {
            "role": "system",
            "content": f"You are an impressive and thorough software development assistant. Here is a snapshot of a repository: {snapshot}",
        },
        {
            "role": "user",
            "content": f"Answer the following question about the code: {question}",
        },
    ]
    return get_gpt4_suggestions(messages)


def main():
    parser = argparse.ArgumentParser(
        description="Ask questions about a git repo using GPT-4."
    )
    parser.add_argument(
        "question", type=str, help="User question about the code"
    )
    parser.add_argument(
        "--repo",
        default=".",
        help="Path to the git repository (default: current directory)",
    )
    args = parser.parse_args()

    repo_path = args.repo
    question = args.question

    try:
        snapshot = get_repo_snapshot(repo_path)
        answer = interact_with_gpt(snapshot, question)
        print(answer)

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
