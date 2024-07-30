from openai import OpenAI

from dotenv import load_dotenv
import os

# I'm using .env file for protection data
load_dotenv()

# API_KEY and BASE_URL is a my own API access to LLM model
client = OpenAI(
    api_key=os.getenv('API_KEY'),
    base_url=os.getenv('BASE_URL'),
)


def llm(history: list[dict]) -> str:
    if not history:
        history = []

    messages = [{
        'role': 'system',
        'content': (
            'AnonLLM provides context-aware responses based on a continuous memory of the conversation. '
            'It remembers all messages sent by the user and responds primarily based on the most recent interaction '
            'while considering context from previous messages. '
            'Mentioning all memorized data in every response is not necessary, '
            'but keeping it in mind for future interactions is important. '
            'Prioritize the last question and answer.'
        )
    }] + history

    # MODEL is some LLM model which I'm using
    response = client.chat.completions.create(
        model=os.getenv('MODEL'),
        messages=messages,
    )

    return response.choices[0].message.content
