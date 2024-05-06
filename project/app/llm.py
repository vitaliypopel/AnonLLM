from openai import OpenAI

from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv('API_KEY'),
    base_url=os.getenv('BASE_URL'),
)


def llm(prompt: str, history: list[dict]) -> str:
    if not history:
        history = []

    messages = history

    messages.insert(0, {
        'role': 'system',
        'content': 'AnonLLM is designed to provide anonymous, context-aware responses '
                   'based on a continuous memory of the conversation. It should remember '
                   'all messages sent by the user and primarily respond based on the most '
                   'recent interaction while considering the context provided by previous messages. '
                   'It is not necessary to mention all the above memorized data in every message, '
                   'but it is important to remember them for possible future reference. '
                   'Priority is given to the last asked question and its answer.'})

    messages.append({'role': 'user', 'content': prompt})

    response = client.chat.completions.create(
        model='llama-13b-chat',
        messages=messages
    )

    return response.choices[0].message.content
