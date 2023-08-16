from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from imgquiz.models import HelloWorld
from django.urls import reverse

def hello_world(request):
    if request.method == 'POST':

        get = request.POST.get('hello_world')
        new_hello_world = HelloWorld()
        new_hello_world.text = get
        new_hello_world.save()

        return HttpResponseRedirect(reverse('imgquiz:hello_world'))
    else:
        return render(request, 'imgquiz/hello_world.html', context={'hello_world_list': HelloWorld.objects.all()})
