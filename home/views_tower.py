from django.shortcuts import render, redirect

from accounts.forms import ProfileForm

def index(request):
    return render(request, 'tower/home.html', {})


def mytracks(request):
    return render(request, 'tower/mytracks.html', {})


def post(request):
    return render(request, 'tower/post.html', {})

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


def dashboard(request):
    return render(request, 'tower/dashboard.html', {})

def post_select(request):
    return render(request, 'tower/select.html', {})

def post_new(request):
    return render(request, 'tower/new.html', {})