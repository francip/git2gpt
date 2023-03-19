from dotenv import load_dotenv
import tiktoken
import time

load_dotenv() # this must run before openai is imported
import openai # this must be loaded after load_dotenv is called

MODEL_NAME = "gpt-4"

encoding = tiktoken.encoding_for_model(MODEL_NAME)

def num_tokens_from_messages(messages, model="gpt-3.5-turbo-0301"):
    """Returns the number of tokens used by a list of messages."""
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        encoding = tiktoken.get_encoding("cl100k_base")
    # this is how gpt-3.5-turbo-0301 works, might be different for future models.
    num_tokens = 0
    for message in messages:
        num_tokens += 4  # every message follows <im_start>{role/name}\n{content}<im_end>\n
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))
            if key == "name":  # if there's a name, the role is omitted
                num_tokens += -1  # role is always required and always 1 token
    num_tokens += 2  # every reply is primed with <im_start>assistant
    return num_tokens

def get_gpt4_suggestions(messages):
    initial_tokens = num_tokens_from_messages(messages, model=MODEL_NAME)
    print(f'Tokens used for the initial request: {initial_tokens}')
    max_tokens = 8192
    avail_tokens = max_tokens - initial_tokens

    # Record the start time
    start_time = time.time()

    response = openai.ChatCompletion.create(
        model=MODEL_NAME,
        messages=messages,
        max_tokens=avail_tokens,
    )

    # Calculate and print the time taken
    time_taken = time.time() - start_time
    print(f'Time taken for the API call: {time_taken:.2f} seconds')
    print(f'{response["usage"]["prompt_tokens"]} prompt tokens used.')
    print(f'Model: {MODEL_NAME}')
    print(f'prompt_tokens: {response["usage"]["prompt_tokens"]}')
    print(f'completion_tokens: {response["usage"]["completion_tokens"]}')
    return response["choices"][0]["message"]["content"]
