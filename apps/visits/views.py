from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.utils import timezone

from .models import Visit, ExamNotes, Manipulation, Vaccination, Prescription, LabResult, Attachment, Deworming, VisitLog
from .forms import (VisitForm, ExamNotesForm, ManipulationForm, VaccinationForm,
                   PrescriptionForm, LabResultForm, AttachmentForm, DewormingForm)
from django.http import JsonResponse
from apps.patients.models import Patient


@login_required
def visit_list(request):
    """List all visits with filtering."""
    query = request.GET.get('q', '')
    status_filter = request.GET.get('status', '')
    date_filter = request.GET.get('date', '')

    visits = Visit.objects.select_related('patient', 'patient__owner', 'veterinarian').all()

    if query:
        visits = visits.filter(
            Q(patient__name__icontains=query) |
            Q(patient__owner__name__icontains=query) |
            Q(reason__icontains=query)
        )

    if status_filter:
        visits = visits.filter(status=status_filter)

    if date_filter == 'today':
        today = timezone.now().date()
        visits = visits.filter(date__date=today)
    elif date_filter == 'week':
        from datetime import timedelta
        week_ago = timezone.now() - timedelta(days=7)
        visits = visits.filter(date__gte=week_ago)

    paginator = Paginator(visits, 20)
    page = request.GET.get('page')
    visits = paginator.get_page(page)

    return render(request, 'visits/visit_list.html', {
        'visits': visits,
        'query': query,
        'status_filter': status_filter,
        'date_filter': date_filter,
        'status_choices': Visit.Status.choices,
    })


@login_required
def visit_detail(request, pk):
    """View visit details with all medical records."""
    visit = get_object_or_404(
        Visit.objects.select_related('patient', 'patient__owner', 'veterinarian'),
        pk=pk
    )

    # Get related records
    try:
        exam_notes = visit.exam_notes
    except ExamNotes.DoesNotExist:
        exam_notes = None

    manipulations = visit.manipulations.all()
    vaccinations = visit.vaccinations.all()
    prescriptions = visit.prescriptions.all()
    lab_results = visit.lab_results.all()
    attachments = visit.attachments.all()
    dewormings = visit.dewormings.all()
    visit_logs = visit.logs.select_related('user').all()[:20]

    return render(request, 'visits/visit_detail.html', {
        'visit': visit,
        'exam_notes': exam_notes,
        'manipulations': manipulations,
        'vaccinations': vaccinations,
        'prescriptions': prescriptions,
        'lab_results': lab_results,
        'attachments': attachments,
        'dewormings': dewormings,
        'visit_logs': visit_logs,
    })


@login_required
def visit_create(request):
    """Create a new visit."""
    initial = {}
    patient_id = request.GET.get('patient')
    if patient_id:
        initial['patient'] = patient_id

    if request.method == 'POST':
        form = VisitForm(request.POST)
        if form.is_valid():
            visit = form.save(commit=False)
            visit.veterinarian = request.user
            visit.save()

            # Log the creation
            VisitLog.objects.create(
                visit=visit,
                user=request.user,
                action=VisitLog.ActionType.CREATED,
                description=f'Преглед създаден от {request.user.get_full_name() or request.user.username}'
            )

            messages.success(request, 'Прегледът е създаден успешно.')
            return redirect('visits:detail', pk=visit.pk)
    else:
        form = VisitForm(initial=initial)

    return render(request, 'visits/visit_form.html', {
        'form': form,
        'title': 'Създаване на нов преглед',
    })


@login_required
def visit_update(request, pk):
    """Update a visit."""
    visit = get_object_or_404(Visit, pk=pk)
    old_status = visit.status

    if request.method == 'POST':
        form = VisitForm(request.POST, instance=visit)
        if form.is_valid():
            form.save()

            # Log updates
            if old_status != visit.status:
                VisitLog.objects.create(
                    visit=visit,
                    user=request.user,
                    action=VisitLog.ActionType.STATUS_CHANGE,
                    description=f'Статус променен от {dict(Visit.Status.choices).get(old_status)} на {visit.get_status_display()} от {request.user.get_full_name() or request.user.username}'
                )
            else:
                VisitLog.objects.create(
                    visit=visit,
                    user=request.user,
                    action=VisitLog.ActionType.UPDATED,
                    description=f'Преглед обновен от {request.user.get_full_name() or request.user.username}'
                )

            messages.success(request, 'Прегледът е обновен успешно.')
            return redirect('visits:detail', pk=visit.pk)
    else:
        form = VisitForm(instance=visit)

    return render(request, 'visits/visit_form.html', {
        'form': form,
        'title': 'Редакция на преглед',
        'visit': visit,
    })


@login_required
def visit_delete(request, pk):
    """Delete a visit."""
    visit = get_object_or_404(Visit, pk=pk)

    if request.method == 'POST':
        patient = visit.patient
        visit.delete()
        messages.success(request, 'Прегледът е изтрит успешно.')
        return redirect('patients:detail', pk=patient.pk)

    return render(request, 'visits/visit_confirm_delete.html', {
        'visit': visit,
    })


# --- Exam Notes ---
@login_required
def add_exam_notes(request, pk):
    """Add or update exam notes for a visit."""
    visit = get_object_or_404(Visit, pk=pk)

    try:
        exam_notes = visit.exam_notes
    except ExamNotes.DoesNotExist:
        exam_notes = None

    if request.method == 'POST':
        form = ExamNotesForm(request.POST, instance=exam_notes)
        if form.is_valid():
            notes = form.save(commit=False)
            notes.visit = visit
            notes.save()

            # Log the action
            VisitLog.objects.create(
                visit=visit,
                user=request.user,
                action=VisitLog.ActionType.EXAM_NOTES,
                description=f'Бележки от преглед {"обновени" if exam_notes else "добавени"} от {request.user.get_full_name() or request.user.username}'
            )

            messages.success(request, 'Бележките от прегледа са запазени успешно.')
            return redirect('visits:detail', pk=visit.pk)
    else:
        form = ExamNotesForm(instance=exam_notes)

    return render(request, 'visits/add_exam_notes.html', {
        'form': form,
        'visit': visit,
    })


# --- Manipulations ---
@login_required
def add_manipulation(request, pk):
    """Add a manipulation/procedure to a visit."""
    visit = get_object_or_404(Visit, pk=pk)

    if request.method == 'POST':
        form = ManipulationForm(request.POST)
        if form.is_valid():
            manipulation = form.save(commit=False)
            manipulation.visit = visit
            manipulation.performed_by = request.user
            manipulation.save()

            # Log the action
            VisitLog.objects.create(
                visit=visit,
                user=request.user,
                action=VisitLog.ActionType.MANIPULATION,
                description=f'Манипулация добавена: {manipulation.name} от {request.user.get_full_name() or request.user.username}'
            )

            messages.success(request, 'Манипулацията е записана успешно.')
            return redirect('visits:detail', pk=visit.pk)
    else:
        form = ManipulationForm()

    return render(request, 'visits/add_manipulation.html', {
        'form': form,
        'visit': visit,
    })


# --- Vaccinations ---
@login_required
def add_vaccination(request, pk):
    """Add a vaccination record to a visit."""
    visit = get_object_or_404(Visit, pk=pk)

    if request.method == 'POST':
        form = VaccinationForm(request.POST)
        if form.is_valid():
            vaccination = form.save(commit=False)
            vaccination.visit = visit
            vaccination.patient = visit.patient
            vaccination.administered_by = request.user
            vaccination.save()

            # Log the action
            VisitLog.objects.create(
                visit=visit,
                user=request.user,
                action=VisitLog.ActionType.VACCINATION,
                description=f'Ваксинация добавена: {vaccination.vaccine_name} от {request.user.get_full_name() or request.user.username}'
            )

            messages.success(request, 'Ваксинацията е записана успешно.')
            return redirect('visits:detail', pk=visit.pk)
    else:
        form = VaccinationForm()

    return render(request, 'visits/add_vaccination.html', {
        'form': form,
        'visit': visit,
    })


# --- Prescriptions ---
@login_required
def add_prescription(request, pk):
    """Add a prescription to a visit."""
    visit = get_object_or_404(Visit, pk=pk)

    if request.method == 'POST':
        form = PrescriptionForm(request.POST)
        if form.is_valid():
            prescription = form.save(commit=False)
            prescription.visit = visit
            prescription.patient = visit.patient
            prescription.prescribed_by = request.user
            prescription.save()
            messages.success(request, 'Рецептата е добавена успешно.')
            return redirect('visits:detail', pk=visit.pk)
    else:
        form = PrescriptionForm()

    return render(request, 'visits/add_prescription.html', {
        'form': form,
        'visit': visit,
    })


# --- Lab Results ---
@login_required
def add_lab_result(request, pk):
    """Add a lab result to a visit."""
    visit = get_object_or_404(Visit, pk=pk)

    if request.method == 'POST':
        form = LabResultForm(request.POST, request.FILES)
        if form.is_valid():
            lab_result = form.save(commit=False)
            lab_result.visit = visit
            lab_result.uploaded_by = request.user
            lab_result.save()
            messages.success(request, 'Лабораторният резултат е качен успешно.')
            return redirect('visits:detail', pk=visit.pk)
    else:
        form = LabResultForm()

    return render(request, 'visits/add_lab_result.html', {
        'form': form,
        'visit': visit,
    })


# --- Attachments ---
@login_required
def add_attachment(request, pk):
    """Add an attachment to a visit."""
    visit = get_object_or_404(Visit, pk=pk)

    if request.method == 'POST':
        form = AttachmentForm(request.POST, request.FILES)
        if form.is_valid():
            attachment = form.save(commit=False)
            attachment.visit = visit
            attachment.uploaded_by = request.user
            attachment.save()
            messages.success(request, 'Прикаченият файл е качен успешно.')
            return redirect('visits:detail', pk=visit.pk)
    else:
        form = AttachmentForm()

    return render(request, 'visits/add_attachment.html', {
        'form': form,
        'visit': visit,
    })


# --- History Views ---
@login_required
def prescription_history(request, patient_pk):
    """View prescription history for a patient."""
    patient = get_object_or_404(Patient, pk=patient_pk)
    prescriptions = Prescription.objects.filter(patient=patient).select_related('visit', 'prescribed_by')

    return render(request, 'visits/prescription_history.html', {
        'patient': patient,
        'prescriptions': prescriptions,
    })


@login_required
def vaccination_history(request, patient_pk):
    """View vaccination history for a patient."""
    patient = get_object_or_404(Patient, pk=patient_pk)
    vaccinations = Vaccination.objects.filter(patient=patient).select_related('visit', 'administered_by')

    return render(request, 'visits/vaccination_history.html', {
        'patient': patient,
        'vaccinations': vaccinations,
    })


# --- Deworming ---
@login_required
def add_deworming(request, pk):
    """Add a deworming/decontamination record to a visit."""
    visit = get_object_or_404(Visit, pk=pk)

    if request.method == 'POST':
        form = DewormingForm(request.POST)
        if form.is_valid():
            deworming = form.save(commit=False)
            deworming.visit = visit
            deworming.patient = visit.patient
            deworming.administered_by = request.user
            deworming.save()

            # Log the action
            VisitLog.objects.create(
                visit=visit,
                user=request.user,
                action=VisitLog.ActionType.DEWORMING,
                description=f'Добавено обезпаразитяване: {deworming.product_name}'
            )

            messages.success(request, 'Обезпаразитяването е записано успешно.')
            return redirect('visits:detail', pk=visit.pk)
    else:
        form = DewormingForm()

    return render(request, 'visits/add_deworming.html', {
        'form': form,
        'visit': visit,
    })


@login_required
def deworming_history(request, patient_pk):
    """View deworming history for a patient."""
    patient = get_object_or_404(Patient, pk=patient_pk)
    dewormings = Deworming.objects.filter(patient=patient).select_related('visit', 'administered_by')

    return render(request, 'visits/deworming_history.html', {
        'patient': patient,
        'dewormings': dewormings,
    })


# --- Autocomplete endpoints ---
@login_required
def manipulation_autocomplete(request):
    """API endpoint for manipulation name autocomplete."""
    query = request.GET.get('q', '')

    manipulation_names = Manipulation.objects.filter(
        name__icontains=query
    ).values_list('name', flat=True).distinct()[:10]

    return JsonResponse({'results': list(manipulation_names)})
