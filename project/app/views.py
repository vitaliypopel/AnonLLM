from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from .models import Message

from openai import InternalServerError

from http.cookies import SimpleCookie
from hashlib import md5
import json

from .llm import llm


def get_session_id(request: HttpRequest) -> str:
    cookie_string = request.headers.get('Cookie')

    cookie = SimpleCookie()
    cookie.load(cookie_string)
    csrf = cookie['csrftoken'].value

    return md5(csrf.encode()).hexdigest()


def get_history(messages: list[Message]) -> list[dict]:
    history = []
    for message in messages:
        history.append({'role': 'user', 'content': message.question})
        history.append({'role': 'assistant', 'content': message.answer})

    return history


@require_http_methods(['GET'])
def chat(request: HttpRequest) -> HttpResponse:
    session_id = get_session_id(request)
    messages = Message.objects.filter(session_id=session_id)
    messages.delete()
    return render(request, 'app/home.html')


@require_http_methods(['POST'])
def llm_api(request: HttpRequest) -> JsonResponse:
    session_id = get_session_id(request)

    body = json.loads(request.body)
    question = body.get('question', '')

    messages = Message.objects.filter(session_id=session_id)
    history = get_history(messages)

    try:
        answer = llm(question, history)
    except InternalServerError:
        return JsonResponse({'error': 'Something went wrong.. Try again'})

    response = {'answer': answer}

    message = Message(
        session_id=session_id,
        question=question,
        answer=answer,
    )
    message.save()

    return JsonResponse(response)
