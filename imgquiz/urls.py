from django.urls import path

from imgquiz.views import hello_world, show_images, next_image,prev_image

app_name = 'imgquiz'

urlpatterns = [
    path('main/', hello_world, name='hello_world'),
    path('show/', show_images, name='show-images'),
    path('next-image/<int:image_index>', next_image, name='next-image'),
    path('prev-image/<int:image_index>', prev_image, name='prev-image'),
]