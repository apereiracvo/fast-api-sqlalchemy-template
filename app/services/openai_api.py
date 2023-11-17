import time
from typing import List, Tuple

import openai

from app.config import settings
from app.services.utils import get_prompt_from_csv
from app.utils.context_vars import token_count


API_TRIES = 5
BACK_OFF = 10  # Seconds to back-off after retry

# region Entry Functions


async def generate_section_gpt(
    section: str,
    client_info: str,
    keywords: str,
    sessions_number: int,
    text_until_now: str,
    terminology: str,
    location_instructions: str = "",
) -> str:
    """Generates a specific note section"""
    SYSTEM_MESSAGES: dict = get_prompt_from_csv(settings.SYSTEM_MESSAGES_PATH)

    PROMPT_TEMPLATES: dict = get_prompt_from_csv(settings.PROMPT_TEMPLATES_PATH)

    GENERAL_MESSAGES: dict = get_prompt_from_csv(settings.GENERAL_MESSAGE_PATH)

    NOTE_STRUCTURE: dict = get_prompt_from_csv(settings.NOTE_STRUCTURE_PATH)

    SECTION_CONTEXTS: dict = get_prompt_from_csv(settings.SECTION_CONTEXTS_PATH)

    USER_FEEDBACK: dict = get_prompt_from_csv(settings.USER_FEEDBACK_PATH)

    TASKS: dict = get_prompt_from_csv(settings.TASKS_PATH)

    WORKFLOW: dict = get_prompt_from_csv(settings.WORKFLOW_PATH)

    # Convert the section name to a valid variable name
    section_name = section.replace(" ", "_").lower()

    prompt = PROMPT_TEMPLATES["general"]
    prompt = prompt.replace("{general_message}", GENERAL_MESSAGES["basic"])
    prompt = prompt.replace("{note_structure}", NOTE_STRUCTURE["basic"])
    prompt = prompt.replace("{terminology}", terminology)
    prompt = prompt.replace("{workflow}", WORKFLOW["basic"])
    prompt = prompt.replace("{client_info}", client_info)
    prompt = prompt.replace("{keywords}", keywords)
    prompt = prompt.replace("{text_until_now}", text_until_now)
    prompt = prompt.replace("{section_context}", SECTION_CONTEXTS[section_name])
    prompt = prompt.replace("{user_feedback}", USER_FEEDBACK[section_name] + location_instructions)
    prompt = prompt.replace("{task}", TASKS["generate"])

    # Set the actual section name
    prompt = prompt.replace("{section}", section)
    prompt = prompt.replace("{number}", str(sessions_number))

    section_text = await call_gpt_api(SYSTEM_MESSAGES["general"], prompt)

    return section_text


async def add_extra_details_gpt(
    actual_text: str,
    details: str,
    client_info: str,
    keywords: str,
    sessions_number: int,
    terminology: str,
    location_instructions: str = "",
):
    """Generates a new intervention with the extra details"""
    SYSTEM_MESSAGES: dict = get_prompt_from_csv(settings.SYSTEM_MESSAGES_PATH)

    PROMPT_TEMPLATES: dict = get_prompt_from_csv(settings.PROMPT_TEMPLATES_PATH)

    GENERAL_MESSAGES: dict = get_prompt_from_csv(settings.GENERAL_MESSAGE_PATH)

    NOTE_STRUCTURE: dict = get_prompt_from_csv(settings.NOTE_STRUCTURE_PATH)

    SECTION_CONTEXTS: dict = get_prompt_from_csv(settings.SECTION_CONTEXTS_PATH)

    USER_FEEDBACK: dict = get_prompt_from_csv(settings.USER_FEEDBACK_PATH)

    TASKS: dict = get_prompt_from_csv(settings.TASKS_PATH)

    WORKFLOW: dict = get_prompt_from_csv(settings.WORKFLOW_PATH)

    prompt = PROMPT_TEMPLATES["details"]
    prompt = prompt.replace("{general_message}", GENERAL_MESSAGES["basic"])
    prompt = prompt.replace("{note_structure}", NOTE_STRUCTURE["basic"])
    prompt = prompt.replace("{terminology}", terminology)
    prompt = prompt.replace("{workflow}", WORKFLOW["details"])
    prompt = prompt.replace("{client_info}", client_info)
    prompt = prompt.replace("{keywords}", keywords)
    prompt = prompt.replace("{text}", actual_text)
    prompt = prompt.replace("{details}", details)
    prompt = prompt.replace("{context}", SECTION_CONTEXTS["details"])
    prompt = prompt.replace("{user_feedback}", USER_FEEDBACK["intervention"] + location_instructions)
    prompt = prompt.replace("{task}", TASKS["details"])

    # Set the actual section name
    prompt = prompt.replace("{number}", str(sessions_number))

    new_text = await call_gpt_api(SYSTEM_MESSAGES["general"], prompt)

    return new_text


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
