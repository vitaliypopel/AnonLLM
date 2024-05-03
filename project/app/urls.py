from django.urls import path

from . import views


app_name = 'app'
urlpatterns = [
    path('', views.chat, name='home'),
    path('chat/', views.chat, name='chat'),
]
