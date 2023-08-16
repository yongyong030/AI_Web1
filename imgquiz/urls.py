from django.urls import path

from imgquiz.views import hello_world

app_name = 'imgquiz'

urlpatterns = [
    path('hello_world/', hello_world, name='hello_world')
]