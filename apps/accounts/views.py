from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.urls import reverse_lazy

from .models import User
from .forms import CustomAuthenticationForm, UserCreateForm, UserUpdateForm, StaffUpdateForm
from .decorators import admin_required


class CustomLoginView(LoginView):
    """Custom login view."""
    form_class = CustomAuthenticationForm
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True


def logout_view(request):
    """Logout view."""
    logout(request)
    messages.success(request, 'Излязохте успешно от системата.')
    return redirect('accounts:login')


@login_required
def profile_view(request):
    """View and edit current user profile."""
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профилът е обновен успешно.')
            return redirect('accounts:profile')
    else:
        form = UserUpdateForm(instance=request.user)

    return render(request, 'accounts/profile.html', {'form': form})


@login_required
@admin_required
def staff_list_view(request):
    """List all staff members (admin only)."""
    staff = User.objects.all()
    return render(request, 'accounts/staff_list.html', {'staff': staff})


@login_required
@admin_required
def staff_create_view(request):
    """Create new staff member (admin only)."""
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'Служител "{user.get_full_name()}" е създаден успешно.')
            return redirect('accounts:staff_list')
    else:
        form = UserCreateForm()

    return render(request, 'accounts/staff_form.html', {'form': form, 'title': 'Добавяне на служител'})


@login_required
@admin_required
def staff_update_view(request, pk):
    """Update staff member (admin only)."""
    user = get_object_or_404(User, pk=pk)

    if request.method == 'POST':
        form = StaffUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, f'Служител "{user.get_full_name()}" е обновен успешно.')
            return redirect('accounts:staff_list')
    else:
        form = StaffUpdateForm(instance=user)

    return render(request, 'accounts/staff_form.html', {'form': form, 'title': 'Редакция на служител', 'user_obj': user})


@login_required
@admin_required
def staff_delete_view(request, pk):
    """Delete staff member (admin only)."""
    user = get_object_or_404(User, pk=pk)

    if user == request.user:
        messages.error(request, 'Не можете да изтриете собствения си акаунт.')
        return redirect('accounts:staff_list')

    if request.method == 'POST':
        name = user.get_full_name()
        user.delete()
        messages.success(request, f'Служител "{name}" е изтрит успешно.')
        return redirect('accounts:staff_list')

    return render(request, 'accounts/staff_confirm_delete.html', {'user_obj': user})
