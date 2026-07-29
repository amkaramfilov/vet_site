from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse

from .models import Patient, WeightRecord
from .forms import PatientForm, WeightRecordForm
from apps.clients.models import Client


@login_required
def patient_list(request):
    """List all patients with search functionality."""
    query = request.GET.get('q', '')
    species_filter = request.GET.get('species', '')

    patients = Patient.objects.select_related('owner').all()

    if query:
        patients = patients.filter(
            Q(name__icontains=query) |
            Q(owner__name__icontains=query) |
            Q(microchip_number__icontains=query)
        )

    if species_filter:
        patients = patients.filter(species__icontains=species_filter)

    # Get distinct species for filter dropdown
    species_list = Patient.objects.values_list('species', flat=True).distinct().order_by('species')

    paginator = Paginator(patients, 20)
    page = request.GET.get('page')
    patients = paginator.get_page(page)

    return render(request, 'patients/patient_list.html', {
        'patients': patients,
        'query': query,
        'species_filter': species_filter,
        'species_choices': [(s, s) for s in species_list],
    })


@login_required
def patient_detail(request, pk):
    """View patient details with medical history."""
    patient = get_object_or_404(Patient.objects.select_related('owner'), pk=pk)
    weight_history = patient.weight_history.all()[:10]
    # Prefetch exam_notes for summary display
    from django.db.models import Prefetch
    from apps.visits.models import ExamNotes, Vaccination, Deworming
    visits = patient.visits.select_related('veterinarian').prefetch_related(
        Prefetch('exam_notes', queryset=ExamNotes.objects.all())
    ).all()[:10]

    # Get vaccinations for this patient
    vaccinations = Vaccination.objects.filter(patient=patient).select_related('visit', 'administered_by')[:5]

    # Get last deworming
    last_deworming = Deworming.objects.filter(patient=patient).first()

    return render(request, 'patients/patient_detail.html', {
        'patient': patient,
        'weight_history': weight_history,
        'visits': visits,
        'vaccinations': vaccinations,
        'last_deworming': last_deworming,
    })


@login_required
def patient_create(request):
    """Create a new patient."""
    initial = {}
    client_id = request.GET.get('client')
    if client_id:
        initial['owner'] = client_id

    if request.method == 'POST':
        form = PatientForm(request.POST, request.FILES)
        if form.is_valid():
            patient = form.save(commit=False)
            patient.created_by = request.user
            patient.save()
            messages.success(request, f'Пациент "{patient.name}" е създаден успешно.')
            return redirect('patients:detail', pk=patient.pk)
    else:
        form = PatientForm(initial=initial)

    return render(request, 'patients/patient_form.html', {
        'form': form,
        'title': 'Добавяне на нов пациент',
    })


@login_required
def patient_update(request, pk):
    """Update an existing patient."""
    patient = get_object_or_404(Patient, pk=pk)

    if request.method == 'POST':
        form = PatientForm(request.POST, request.FILES, instance=patient)
        if form.is_valid():
            form.save()
            messages.success(request, f'Пациент "{patient.name}" е обновен успешно.')
            return redirect('patients:detail', pk=patient.pk)
    else:
        form = PatientForm(instance=patient)

    return render(request, 'patients/patient_form.html', {
        'form': form,
        'title': 'Редакция на пациент',
        'patient': patient,
    })


@login_required
def patient_delete(request, pk):
    """Delete a patient."""
    patient = get_object_or_404(Patient, pk=pk)

    if request.method == 'POST':
        name = patient.name
        owner = patient.owner
        patient.delete()
        messages.success(request, f'Пациент "{name}" е изтрит успешно.')
        return redirect('clients:detail', pk=owner.pk)

    return render(request, 'patients/patient_confirm_delete.html', {
        'patient': patient,
    })


@login_required
def add_weight(request, pk):
    """Add a weight record for a patient."""
    patient = get_object_or_404(Patient, pk=pk)

    if request.method == 'POST':
        form = WeightRecordForm(request.POST)
        if form.is_valid():
            weight_record = form.save(commit=False)
            weight_record.patient = patient
            weight_record.recorded_by = request.user
            weight_record.save()
            messages.success(request, f'Записът за тегло на {patient.name} е добавен.')
            return redirect('patients:detail', pk=patient.pk)
    else:
        form = WeightRecordForm()

    return render(request, 'patients/add_weight.html', {
        'form': form,
        'patient': patient,
    })


@login_required
def weight_history(request, pk):
    """View full weight history for a patient."""
    patient = get_object_or_404(Patient, pk=pk)
    weight_records = patient.weight_history.all()

    # Prepare data for chart
    chart_data = list(weight_records.order_by('recorded_at').values('recorded_at', 'weight'))

    return render(request, 'patients/weight_history.html', {
        'patient': patient,
        'weight_records': weight_records,
        'chart_data': chart_data,
    })


@login_required
def patient_search(request):
    """API endpoint for patient search/autocomplete."""
    query = request.GET.get('q', '')
    if len(query) < 2:
        return JsonResponse({'results': []})

    patients = Patient.objects.select_related('owner').filter(
        Q(name__icontains=query) |
        Q(owner__name__icontains=query) |
        Q(microchip_number__icontains=query)
    )[:10]

    results = [
        {
            'id': patient.pk,
            'name': patient.name,
            'species': patient.species,
            'owner': patient.owner.name,
            'text': f'{patient.name} ({patient.species}) - {patient.owner.name}'
        }
        for patient in patients
    ]

    return JsonResponse({'results': results})


@login_required
def species_autocomplete(request):
    """API endpoint for species autocomplete."""
    query = request.GET.get('q', '')

    # Get distinct species from database
    species_list = Patient.objects.filter(
        species__icontains=query
    ).values_list('species', flat=True).distinct()[:10]

    # Add common species if query matches
    common_species = ['Куче', 'Котка', 'Птица', 'Заек', 'Хамстер', 'Морско свинче', 'Влечуго']
    results = list(species_list)
    for s in common_species:
        if query.lower() in s.lower() and s not in results:
            results.append(s)

    return JsonResponse({'results': results[:10]})


@login_required
def breed_autocomplete(request):
    """API endpoint for breed autocomplete."""
    query = request.GET.get('q', '')
    species = request.GET.get('species', '')

    breeds = Patient.objects.filter(breed__icontains=query)
    if species:
        breeds = breeds.filter(species__iexact=species)

    breed_list = breeds.values_list('breed', flat=True).distinct()[:10]

    return JsonResponse({'results': list(breed_list)})
