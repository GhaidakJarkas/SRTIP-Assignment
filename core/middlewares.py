from django.shortcuts import redirect


#Middleware to protect all the views that require the user to be logged in
class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated and not request.path.endswith('/login/'):
            return redirect('core:login')
        return self.get_response(request)