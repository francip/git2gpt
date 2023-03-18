from dotenv import load_dotenv
from tiktoken import Tokenizer

load_dotenv() # this must run before openai is imported
import openai # this must be loaded after load_dotenv is called

MODEL_NAME = "gpt-4"

tokenizer = Tokenizer()


def count_tokens(text):
    return len(list(tokenizer.tokenize(text)))


def get_gpt4_suggestions(messages):
    initial_tokens = sum([count_tokens(json.dumps(msg)) for msg in messages])
    print(f'Tokens used for the initial request: {initial_tokens}')

    response = openai.ChatCompletion.create(
        model=MODEL_NAME,
        messages=messages,
        max_tokens=4096,
    )

    response_tokens = count_tokens(response['id'])
    print(f'Tokens used for the generated response: {response_tokens}')

    return response["choices"][0]["message"]["content"]
