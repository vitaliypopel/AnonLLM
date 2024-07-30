from django.http import HttpRequest

from .models import Message

from hashlib import md5


def get_session_id(request: HttpRequest) -> str | None:
    # This function is creating unique hashed string for current chat using md5 for hash csrf token

    csrf_token = request.COOKIES.get('csrftoken')

    if csrf_token:
        return md5(csrf_token.encode()).hexdigest()

def get_history(messages: list[Message]) -> list[dict]:
    # History is a history of chat which saved in database for get more detail of current chat for LLM

    history = []
    for message in messages:
        history.append({'role': 'user', 'content': message.question})
        history.append({'role': 'assistant', 'content': message.answer})

    return history
