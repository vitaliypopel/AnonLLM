from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods

from .llm import llm


@require_http_methods(['GET'])
def chat(request: HttpRequest) -> HttpResponse:
    return render(request, 'app/home.html')


@require_http_methods(['POST'])
def llm_api(request: HttpRequest) -> JsonResponse:
    question = request.POST.get('question', '')

    response = {
        'answer': llm(question)
    }

    return JsonResponse(response)
