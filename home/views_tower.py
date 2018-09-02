from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings

from accounts.forms import ProfileForm

import requests
import json

def index(request):
    return render(request, 'tower/home.html', {})

@login_required
def mytracks(request):
    return render(request, 'tower/mytracks.html', {})


@login_required
def post(request):
    return render(request, 'tower/post.html', {})


@login_required
def profile(request):
    if request.method == "POST":
        form = ProfileForm(request.POST)        

        if form.is_valid():
            print(form.cleaned_data)
            
            profile = request.user.profile
            profile.likes_greeting = form.cleaned_data['likes_greeting']
            profile.clips_greeting = form.cleaned_data['clips_greeting']
            profile.nickname = form.cleaned_data['nickname']
            profile.greeting = form.cleaned_data['greeting']
            profile.location = form.cleaned_data['location']
            profile.crew = form.cleaned_data['crew']

            profile.save()
            return redirect('profile')
    else:
        form = ProfileForm()
    return render(request, 'tower/profile.html', {'form': form})


@login_required
def dashboard(request):
    if 0 is request.user.profile.soundcloud_id:
        return redirect('//auth.dopehotz.com/connect/')
    
    return render(request, 'tower/dashboard.html', {})

@login_required
def post_select(request):
    datas = requests.get('http://api.soundcloud.com/users/'+str(request.user.profile.soundcloud_id)+'/tracks/?client_id='+settings.SOCIAL_AUTH_SOUNDCLOUD_KEY)
    post_list = []

    if datas.content:
        post_list = json.loads(datas.content)

    return render(request, 'tower/select.html', {'post_list': post_list})

@login_required
def post_new(request):
    return render(request, 'tower/new.html', {})

@login_required
def connect(request):
    if 0 is not request.user.profile.soundcloud_id:
        return redirect('//tower.dopehotz.com/dashboard/')

    return render(request, 'tower/connect.html', {})