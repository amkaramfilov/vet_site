from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages


def admin_required(view_func):
    """Decorator that checks if user is an admin."""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_admin:
            messages.error(request, 'You do not have permission to access this page.')
            return redirect('core:dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper


def veterinarian_required(view_func):
    """Decorator that checks if user is a veterinarian or admin."""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not (request.user.is_veterinarian or request.user.is_admin):
            messages.error(request, 'You do not have permission to access this page.')
            return redirect('core:dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper
