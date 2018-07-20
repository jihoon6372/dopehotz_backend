from django.shortcuts import render

def index(request):
    return render(request, 'tower/home.html', {})


def mytracks(request):
    return render(request, 'tower/mytracks.html', {})


def post(request):
    return render(request, 'tower/post.html', {})

def profile(request):
    return render(request, 'tower/profile.html', {})

def dashboard(request):
    return render(request, 'tower/dashboard.html', {})

def post_select(request):
    return render(request, 'tower/select.html', {})

def post_new(request):
    return render(request, 'tower/new.html', {})