from django.shortcuts import redirect
from functools import wraps

def role_required(allowed_roles):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if request.user.rôle not in allowed_roles:
                # Redirige l'utilisateur s'il n'a pas le rôle requis
                return redirect('page_non_autorisee')  # Remplacez 'page_non_autorisee' par le nom de votre page d'interdiction d'accès
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator
