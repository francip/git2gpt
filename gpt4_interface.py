from dotenv import load_dotenv

load_dotenv() # this must run before openai is imported

# api key will be loaded from environment via dotenv
import openai

MODEL_NAME = "gpt-4"


def get_gpt4_suggestions(messages):
    response = openai.ChatCompletion.create(
        model=MODEL_NAME,
        messages=messages,
        max_tokens=4096,

    )
    return response["choices"][0]["message"]["content"]
