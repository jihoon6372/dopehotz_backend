from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.db.models import Sum

from accounts.forms import ProfileForm
from tracks.models import Track, TrackLikeLog, TrackComment
from .decorators import connect_required


import requests
import json

def index(request):
    return render(request, 'tower/home.html', {})

@login_required
@connect_required
def mytracks(request, list_type):
    if 'all' in list_type:
        track_list = Track.objects.filter(user=request.user)
    elif 'on-stage' in list_type:
        track_list = Track.objects.filter(user=request.user, on_stage=1)
    elif 'open-mic' in list_type:
        track_list = Track.objects.filter(user=request.user, on_stage=0)
    else:
        track_list = []

    order_type = request.GET.get('order', None)

    if None is not order_type:
        if 'play' in order_type:
            track_list = track_list.order_by('-play_count')
            
        elif 'like' in order_type:
            track_list = track_list.order_by('-like_count')

    return render(request, 'tower/mytracks.html', {'track_list': track_list})


@login_required
@connect_required
def mytracks2(request):
    return render(request, 'tower/mytracks.html')


@login_required
@connect_required
def post(request):
    return render(request, 'tower/post.html', {})


@login_required
@connect_required
def profile(request):
    if request.method == "POST":
        form = ProfileForm(request.POST)

        if form.is_valid():
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
@connect_required
def dashboard(request):
    if 0 is request.user.profile.soundcloud_id:
        return redirect('//auth.dopehotz.com/connect/')

    view_count_data, track_like_log_count, comment_count = 0, 0, 0
    view_count_data = Track.objects.filter(user=request.user).aggregate(Sum('view_count'))

    view_count = 0 if None is view_count_data['view_count__sum'] else view_count_data['view_count__sum']
    track_like_log_count = TrackLikeLog.objects.filter(track__user=request.user).count()
    comment_count = TrackComment.objects.filter(track__user=request.user).count()

    order_track_like_list = Track.objects.filter(user=request.user).order_by('-like_count')[:5]
    order_track_view_list = Track.objects.filter(user=request.user).order_by('-view_count')[:5]

    template_data = {
        'view_count': view_count,
        'track_like_log_count': track_like_log_count,
        'comment_count': comment_count,
        'order_track_like_list': order_track_like_list,
        'order_track_view_list': order_track_view_list
    }
    
    return render(request, 'tower/dashboard.html', template_data)


@login_required
@connect_required
def post_select(request):
    datas = requests.get('http://api.soundcloud.com/users/'+str(request.user.profile.soundcloud_id)+'/tracks/?client_id='+settings.SOCIAL_AUTH_SOUNDCLOUD_KEY)
    post_list = []

    if datas.content:
        post_list = json.loads(datas.content)

    return render(request, 'tower/select.html', {'post_list': post_list})

@login_required
@connect_required
def post_new(request, track_id):
    data = requests.get('http://api.soundcloud.com/tracks/'+str(track_id)+'/?client_id='+settings.SOCIAL_AUTH_SOUNDCLOUD_KEY)

    if data.content:
        track_data = json.loads(data.content)
        
        if None is track_data['artwork_url']:
            track_image = track_data['user']['avatar_url']
        else:
            track_image = track_data['artwork_url']

    template_data = {
        'track_data': track_data,
        'track_image': track_image,
        'track_id': track_id,
        'type': 'create'
    }

    return render(request, 'tower/new.html', template_data)


@login_required
@connect_required
def post_modify(request, track_id):
    track = Track.objects.get(user=request.user, track_id=track_id)
    template_data = {
        'track': track,
        'type': 'update',
        'track_id': track_id,
        'track_image': track.image_url
    }
    return render(request, 'tower/new.html', template_data)


@login_required
def connect(request):
    if 0 is not request.user.profile.soundcloud_id:
        return redirect('//tower.dopehotz.com/dashboard/')

    return render(request, 'tower/connect.html', {})


@login_required
@connect_required
def post_create_done(request):
    return render(request, 'tower/done.html')