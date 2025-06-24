from django.shortcuts import redirect
from django.http import HttpResponseForbidden

def role_required(roles):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')
            if request.user.userprofile.role not in roles:
                return HttpResponseForbidden("⛔ Доступ заборонено")
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
