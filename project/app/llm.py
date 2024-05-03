from openai import OpenAI

from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv('API_KEY'),
    base_url=os.getenv('BASE_URL'),
)


def llm(prompt: str) -> str:
    response = client.chat.completions.create(
        model='llama-13b-chat',
        messages=[
            {'role': 'system', 'content': 'You are a helpful anonymous assistant, called AnonLLM.'},
            {'role': 'user', 'content': prompt},
        ]
    )

    return response.choices[0].message.content
