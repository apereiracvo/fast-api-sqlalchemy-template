import time
from typing import List, Tuple

import openai

from app.config import settings


API_TRIES = 5
BACK_OFF = 10  # Seconds to back-off after retry


# region Entry Functions


async def call_gpt35_turbo(system_message: str, prompt: str) -> Tuple[str, int]:
    """Calls OpenAI GPT3.5 turbo API with the specified system message and prompt"""
    result = ""
    tries = 0
    tokens = 0
    while not result and tries < API_TRIES:
        try:
            openai.api_key = settings.OPENAI_API_KEY
            response = await openai.ChatCompletion.acreate(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": prompt},
                ],
            )
            result = response["choices"][0]["message"]["content"]
            tokens = response["usage"]["total_tokens"]
        except Exception as e:
            print(str(e))
            tries += 1
    return result, tokens


async def call_gpt3_davinci(system_message: str, prompt: str) -> Tuple[str, int]:
    """Calls OpenAI GPT-3 Davinci API with the specified system message and prompt"""
    tries = 0
    result = ""
    tokens = 0
    prompt = f"{system_message}\n\n{prompt}"
    while not result and tries < API_TRIES:
        try:
            openai.api_key = settings.OPENAI_API_KEY
            response = await openai.Completion.acreate(
                model="text-davinci-003",
                prompt=prompt,
                temperature=0.0,
                max_tokens=1000,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0,
            )
            result = response["choices"][0]["text"]
            tokens = response["usage"]["total_tokens"]
        except Exception as e:
            print(str(e))
            tries += 1
    return result, tokens


async def call_gpt4(system_message: str, prompt: str) -> Tuple[str, int]:
    """Calls OpenAI GPT-4 API with the specified system message and prompt"""
    result = ""
    tokens = 0
    tries = 0
    back_off = 1
    while not result and tries < API_TRIES:
        try:
            openai.api_key = settings.OPENAI_API_KEY
            response = await openai.ChatCompletion.acreate(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.5,
                top_p=1,
            )
            result = response["choices"][0]["message"]["content"]
            tokens = response["usage"]["total_tokens"]
        except Exception as e:
            print(str(e))
            tries += 1
            time.sleep(BACK_OFF * back_off)
            back_off += 1
    return result, tokens


async def call_gpt_api(system_message: str, prompt: str) -> str:
    """Selects and calls the correct GPT model to use from settings"""
    current_count = token_count.get()
    if settings.GPT_MODEL == "gpt3.5":
        # GPT3.5
        result, tokens = await call_gpt35_turbo(system_message, prompt)
    elif settings.GPT_MODEL == "davinci":
        # GPT3 Davinci
        result, tokens = await call_gpt3_davinci(system_message, prompt)
    else:
        # GPT-4
        result, tokens = await call_gpt4(system_message, prompt)

    # Add token count
    token_count.set(current_count + tokens)

    # print("====PROMPT DEBUG===")
    # print(f"Model: {settings.GPT_MODEL}\n\n")
    # print(f"System Message: {system_message}\n\n")
    # print(f"System Message: {prompt}\n\n")
    # Return result
    return result


# endregion

# region Utility Functions


async def get_embeddings(text: str) -> List:
    # initialize the OpenAI API client
    openai.api_key = settings.OPENAI_API_KEY
    # get the embeddings using the OpenAI API
    response = await openai.Embedding.acreate(
        model="text-embedding-ada-002",
        input=text,
    )
    return response["data"][0]["embedding"]


async def get_embeddings_list(text_list: List[str]) -> List:
    # initialize the OpenAI API client
    openai.api_key = settings.OPENAI_API_KEY
    # get the embeddings using the OpenAI API
    response = await openai.Embedding.acreate(
        model="text-embedding-ada-002",
        input=text_list,
    )
    return response["data"]


# endregion
