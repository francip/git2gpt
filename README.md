This repository is an MVP to bootstrap a self-modifying agent using GPT-4.

MVP features:

- Provide snapshot of the current codebase to GPT-4
- Apply changes from the GPT-4 API

Usage:

1. Install the required packages using pip:
   `pip install -r requirements.txt`
2. Set up your OpenAI API key:
   `echo "OPENAI_API_KEY=your_key_here" > .env`
3. Run the main script:
   `python main.py`

Changelog:

2023/03/16:

- Create a simple script to make a query to OpenAI 3.5 turbo (still waiting on GPT-4 access)
- Add git_to_json.py as the first part of the git2gpt interface
- Add interact_with_gpt function to main.py
- Update README.md with usage instructions and additional details
