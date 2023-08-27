import os

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from imgquiz.models import HelloWorld
from django.urls import reverse
from django.contrib.sessions.models import Session

from web1.settings import BASE_DIR

from PIL import Image
from django.db import transaction

import datetime

from ai import caption, sentence_model
from sentence_transformers.util import cos_sim



def update_image_index(current_date, image_index):
    # 현재 날짜 가져오기
    today = datetime.date.today()

    # 날짜가 하루 지났는지 확인
    if current_date is None or today > current_date:
        # 날짜가 하루 지났을 때 이미지 인덱스 증가
        new_image_index = image_index + 1
        HelloWorld.objects.all().delete()
        return today, new_image_index
    else:
        return current_date, image_index

current_date = None
image_index = 1
current_date, image_index = update_image_index(current_date, image_index)

image_folder = os.path.join(BASE_DIR, 'imgquiz\\static\\val2017\\')
image_files = [f for f in os.listdir(image_folder)]
image_index = min(max(0, int(image_index)), len(image_files) - 1)
current_image = image_files[image_index]

img_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static/val2017/', current_image)
raw_image = Image.open(img_path).convert('RGB')

# 사용자의 IP 주소를 가져오는 함수
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def hello_world(request):
    if request.method == 'POST':

        get = request.POST.get('hello_world')
        new_hello_world = HelloWorld()
        new_hello_world.text = get

        last_answer = get
        sentences = [f'{caption}', f'{last_answer}']
        embeddings = sentence_model.encode(sentences)
        score = cos_sim(embeddings[0], embeddings[1])
        new_hello_world.score = score

        ip = get_client_ip(request)
        new_hello_world.user_ip = ip

        with transaction.atomic():
            new_hello_world.save()

        return HttpResponseRedirect(reverse('imgquiz:hello_world'))
    else:
        if not image_files:
            return render(request, 'imgquiz/main.html', {'image_files': [], 'image_index': None})

        user_ip = get_client_ip(request)
        hello_world_list = list(reversed(HelloWorld.objects.filter(user_ip=user_ip)))

        context = {'image_index': image_index,
                   'current_image': current_image,
                   'image_files': image_files,
                   'caption': caption,
                   'hello_world_list': hello_world_list,
                   }

        return render(request, 'imgquiz/main.html', context)

# def show_images(request, image_index=0):
#     image_folder = os.path.join(BASE_DIR, 'imgquiz\\static\\val2017\\')
#     image_files = [f for f in os.listdir(image_folder)]
#
#     if not image_files:
#         return render(request, 'imgquiz/show.html', {'image_files': [], 'image_index': None})
#
#     image_index = min(max(0, int(image_index)), len(image_files) - 1)
#     current_image = image_files[image_index]
#
#     img_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static/val2017/', current_image)
#     raw_image = Image.open(img_path).convert('RGB')
#
#     # unconditional image captioning
#     inputs = processor(raw_image, return_tensors="pt")
#
#     out = model.generate(**inputs)
#     caption = processor.decode(out[0], skip_special_tokens=True)
#
#     hello_world_list = HelloWorld.objects.all()
#
#     context = {'image_index': image_index,
#                'current_image': current_image,
#                'image_files': image_files,
#                'caption': caption,
#                'hello_world_list': hello_world_list}
#
#
#     return render(request, 'imgquiz/show.html',context)
#
# def next_image(request, image_index):
#     image_index = int(image_index) + 1
#     return show_images(request, image_index)
#
# def prev_image(request, image_index):
#     image_index = int(image_index) - 1
#     return show_images(request, image_index)