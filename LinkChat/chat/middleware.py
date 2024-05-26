
from django.shortcuts import redirect


class RedirectAuthenticatedUserMiddleware:
    def __init__(self , get_response ):
        self.get_response = get_response
        
    def __call__(self,request):
        print(f"Request path: {request.path}, User authenticated: {request.user.is_authenticated}")
        if request.user.is_authenticated and request.path in ['/login', '/login/' , 'login' , '/' , 'register' ]:
            print('kkooooooooooooooo')
            return redirect('home')
        response = self.get_response(request)
        return response
        
        