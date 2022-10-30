from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import redirect,reverse
from django.contrib import messages



def unauthenticated_user(view_func):
    def wrapper_func(request , *args ,**kwargs):
        if request.user.is_authenticated:
            print("authed")
        else:
            return view_func(request ,*args,**kwargs)
    return wrapper_func





def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args ,**kwargs):
            group = None
            if request.user.groups.exists():
                groups = request.user.groups.all()[0].name
           

            if groups in allowed_roles:
                return view_func(request , *args ,**kwargs)

            else:
                return HttpResponse("This account is already used in other services offered by SPOTEZY,,, pls use different account")            

        return wrapper_func
    return decorator

