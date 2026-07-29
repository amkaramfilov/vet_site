from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse

from .models import Client
from .forms import ClientForm


@login_required
def client_list(request):
    """List all clients with search functionality."""
    query = request.GET.get('q', '')
    clients = Client.objects.all()

    if query:
        clients = clients.filter(
            Q(name__icontains=query) |
            Q(phone__icontains=query) |
            Q(email__icontains=query)
        )

    paginator = Paginator(clients, 20)
    page = request.GET.get('page')
    clients = paginator.get_page(page)

    return render(request, 'clients/client_list.html', {
        'clients': clients,
        'query': query,
    })


@login_required
def client_detail(request, pk):
    """View client details and their pets."""
    client = get_object_or_404(Client, pk=pk)
    patients = client.patients.all()

    return render(request, 'clients/client_detail.html', {
        'client': client,
        'patients': patients,
    })


@login_required
def client_create(request):
    """Create a new client."""
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            client = form.save(commit=False)
            client.created_by = request.user
            client.save()
            messages.success(request, f'Клиент "{client.name}" е създаден успешно.')
            return redirect('clients:detail', pk=client.pk)
    else:
        form = ClientForm()

    return render(request, 'clients/client_form.html', {
        'form': form,
        'title': 'Добавяне на нов клиент',
    })


@login_required
def client_update(request, pk):
    """Update an existing client."""
    client = get_object_or_404(Client, pk=pk)

    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            messages.success(request, f'Клиент "{client.name}" е обновен успешно.')
            return redirect('clients:detail', pk=client.pk)
    else:
        form = ClientForm(instance=client)

    return render(request, 'clients/client_form.html', {
        'form': form,
        'title': 'Редакция на клиент',
        'client': client,
    })


@login_required
def client_delete(request, pk):
    """Delete a client."""
    client = get_object_or_404(Client, pk=pk)

    if request.method == 'POST':
        name = client.name
        client.delete()
        messages.success(request, f'Клиент "{name}" е изтрит успешно.')
        return redirect('clients:list')

    return render(request, 'clients/client_confirm_delete.html', {
        'client': client,
    })


@login_required
def client_search(request):
    """API endpoint for client search/autocomplete."""
    query = request.GET.get('q', '')
    if len(query) < 2:
        return JsonResponse({'results': []})

    clients = Client.objects.filter(
        Q(name__icontains=query) |
        Q(phone__icontains=query)
    )[:10]

    results = [
        {
            'id': client.pk,
            'name': client.name,
            'phone': client.phone,
            'text': f'{client.name} ({client.phone})'
        }
        for client in clients
    ]

    return JsonResponse({'results': results})
