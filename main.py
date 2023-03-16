from gpt4_interface import get_gpt4_suggestions

if __name__ == "__main__":
    messages = [
		{"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Write a simple Python function that takes a number and returns its square:"},
    ]
    suggestion = get_gpt4_suggestions(messages)
    print(suggestion)
