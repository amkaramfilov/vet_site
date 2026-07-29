from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta

from apps.clients.models import Client
from apps.patients.models import Patient
from apps.visits.models import Visit


@login_required
def dashboard(request):
    """Main dashboard view with statistics and recent activity."""
    today = timezone.now().date()

    # Statistics
    total_clients = Client.objects.count()
    total_patients = Patient.objects.count()
    today_visits = Visit.objects.filter(date__date=today).count()
    pending_visits = Visit.objects.filter(
        status__in=[Visit.Status.SCHEDULED, Visit.Status.IN_PROGRESS]
    ).count()

    # Recent data
    recent_visits = Visit.objects.select_related(
        'patient', 'veterinarian'
    ).order_by('-date')[:5]

    recent_patients = Patient.objects.select_related(
        'owner'
    ).order_by('-created_at')[:5]

    context = {
        'title': 'Dashboard',
        'total_clients': total_clients,
        'total_patients': total_patients,
        'today_visits': today_visits,
        'pending_visits': pending_visits,
        'recent_visits': recent_visits,
        'recent_patients': recent_patients,
    }
    return render(request, 'core/dashboard.html', context)
