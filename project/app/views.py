from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_http_methods

from .models import Message

from openai import InternalServerError

from http.cookies import SimpleCookie
from hashlib import md5
import json

from .llm import llm


def get_session_id(request: HttpRequest) -> str | None:
    # This function is creating unique hashed string for current chat using md5 for hash csrf token

    cookie_string = request.headers.get('Cookie')
    cookie = SimpleCookie()
    cookie.load(cookie_string)

    try:
        csrf = cookie['csrftoken'].value
        return md5(csrf.encode()).hexdigest()
    except KeyError:
        return None


def get_history(messages: list[Message]) -> list[dict]:
    # History is a history of chat which saved in database for get more detail of current chat for LLM

    history = []
    for message in messages:
        history.append({'role': 'user', 'content': message.question})
        history.append({'role': 'assistant', 'content': message.answer})

    return history


@require_http_methods(['GET'])
@ensure_csrf_cookie
def chat(request: HttpRequest) -> HttpResponse:
    # Main page which reset all messages before and returning html template with chat

    session_id = get_session_id(request)
    if not session_id:
        return HttpResponse('Cannot get access without CSRF token', status=403)

    try:
        messages = Message.objects.filter(session_id=session_id)
        if messages:
            messages.delete()
    except Exception as e:
        print(e)
        return HttpResponse('Something went wrong with database...', status=500)

    return render(request, 'app/home.html')


@require_http_methods(['POST'])
@ensure_csrf_cookie
def llm_api(request: HttpRequest) -> JsonResponse:
    # API for JavaScript for asking LLM model and responding

    session_id = get_session_id(request)
    if not session_id:
        return JsonResponse({'error': 'Cannot get access without CSRF token'}, status=403)

    request_body = json.loads(request.body)
    question = request_body.get('question', '')

    messages = Message.objects.filter(session_id=session_id)
    history = get_history(messages)

    try:
        answer = llm(question, history)
    except InternalServerError:
        return JsonResponse({'error': 'Something went wrong.. Try again'}, status=500)

    response = {'answer': answer}

    # We are saving messages for get more details of current chat session
    try:
        message = Message(
            session_id=session_id,
            question=question,
            answer=answer,
        )
        message.save()
    except Exception as e:
        print(e)
        return JsonResponse({'error': 'Something went wrong with database...'}, status=500)

    return JsonResponse(response)
