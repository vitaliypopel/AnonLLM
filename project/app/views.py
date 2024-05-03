from django.shortcuts import render


def chat(request):
    return render(request, 'app/home.html')
