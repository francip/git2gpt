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

    model_cost_per_token = {
        'gpt-4': {'prompt': 0.03 / 1000, 'completion': 0.06 / 1000},
        'gpt-4-32k': {'prompt': 0.06 / 1000, 'completion': 0.012 / 1000},
        'gpt-3.5-turbo': {'prompt': 0.002 / 1000, 'completion': 0.002 / 1000}
    }

    initial_tokens = num_tokens_from_messages(messages, model=MODEL_NAME)
    print(f'Tokens used for the initial request: {initial_tokens}')
    max_tokens = 8192
    avail_tokens = max_tokens - initial_tokens

    cost_per_prompt_token = model_cost_per_token[MODEL_NAME]['prompt']
    cost_per_completion_token = model_cost_per_token[MODEL_NAME]['completion']

    # Record the start time
    start_time = time.time()

    response = openai.ChatCompletion.create(
        model=MODEL_NAME,
        messages=messages,
        max_tokens=avail_tokens,
    )

    # Calculate and print the time taken
    time_taken = time.time() - start_time
    prompt_tokens = response["usage"]["prompt_tokens"]
    completion_tokens = response["usage"]["completion_tokens"]

    prompt_cost = prompt_tokens * cost_per_prompt_token
    completion_cost = completion_tokens * cost_per_completion_token
    total_cost = prompt_cost + completion_cost

    total_tokens = prompt_tokens + completion_tokens

    print(f'Time taken for the API call: {time_taken:.2f} seconds')
    print(f'{prompt_tokens} prompt tokens used. Cost: ${prompt_cost:.6f}')
    print(f'{completion_tokens} completion tokens used. Cost: ${completion_cost:.6f}')
    print(f'Total cost of the API call: ${total_cost:.6f}')
    print(f'Total tokens used: {total_tokens}')

    print(f'Model: {MODEL_NAME}')
    return response["choices"][0]["message"]["content"]
