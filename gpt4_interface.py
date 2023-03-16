from dotenv import load_dotenv
load_dotenv()

# api key will be loaded from environment via dotenv
import openai

MODEL_NAME="gpt-3.5-turbo"  # Update to GPT-4 when available.

def get_gpt4_suggestions(messages):
    response = openai.ChatCompletion.create(
        model=MODEL_NAME,
        messages=messages,
    )
    return response["choices"][0]["message"]["content"]
