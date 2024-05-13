from django.http import HttpResponse
from django.shortcuts import render

def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            role = request.user.role
            if role in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return render(request, '404.html')

        return wrapper_func
    return decorator