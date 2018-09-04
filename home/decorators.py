from django.shortcuts import redirect

def connect_required(function):
    def wrap(request, *args, **kwargs):
        if 0 is request.user.profile.soundcloud_id:
            return redirect('//auth.dopehotz.com/connect/')
        else:
            return function(request, *args, **kwargs)
    return wrap