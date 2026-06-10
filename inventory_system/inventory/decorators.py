from django.shortcuts import redirect
from django.contrib import messages


def role_required(*allowed_roles):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')
            if request.user.role not in allowed_roles:
                messages.error(request, 'You do not have permission to access this page.')
                return redirect('dashboard')
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator


def admin_required(view_func):
    return role_required('admin')(view_func)


def manager_required(view_func):
    return role_required('admin', 'manager')(view_func)


def staff_or_above(view_func):
    return role_required('admin', 'manager', 'staff')(view_func)
