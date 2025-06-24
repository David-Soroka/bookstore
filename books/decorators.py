from django.shortcuts import redirect
from django.http import HttpResponseForbidden
from django.utils.translation import gettext as _

def role_required(roles):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')
            if request.user.userprofile.role not in roles:
                return HttpResponseForbidden(_("⛔ Доступ заборонено"))
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
