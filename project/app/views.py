from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_http_methods

from openai import InternalServerError
import json

from .llm import llm


@require_http_methods(['GET'])
@ensure_csrf_cookie
def chat(request: HttpRequest) -> HttpResponse:
    # Main page which reset all messages before and returning html template with chat
    return render(request, 'app/home.html')


@require_http_methods(['POST'])
@ensure_csrf_cookie
def llm_api(request: HttpRequest) -> JsonResponse:
    # API for JavaScript for asking LLM model and responding
    request_body = json.loads(request.body)
    history = request_body.get('history', [])

    try:
        answer = llm(history)
    except InternalServerError:
        return JsonResponse({'error': 'Something went wrong.. Try again'}, status=500)

    response = {'answer': answer}

    return JsonResponse(response)
