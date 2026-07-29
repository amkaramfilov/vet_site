from django import forms
from .models import Visit, ExamNotes, Manipulation, Vaccination, Prescription, LabResult, Attachment, Deworming
from apps.patients.models import Patient


class VisitForm(forms.ModelForm):
    """Form for creating and updating visits."""

    patient = forms.ModelChoiceField(
        queryset=Patient.objects.select_related('owner').all(),
        label='Пациент',
        widget=forms.Select(attrs={
            'class': 'form-control patient-select',
            'data-search-url': '/patients/search/',
        }),
        help_text='Търсене по име на пациент, собственик или микрочип'
    )

    class Meta:
        model = Visit
        fields = ['patient', 'date', 'reason', 'status']
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'reason': forms.Textarea(attrs={'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name != 'patient':  # patient is already configured
                field.widget.attrs['class'] = 'form-control'


class ExamNotesForm(forms.ModelForm):
    """Form for exam notes."""

    class Meta:
        model = ExamNotes
        fields = ['symptoms', 'diagnosis', 'treatment_plan', 'follow_up_notes',
                  'temperature', 'heart_rate', 'respiratory_rate']
        widgets = {
            'symptoms': forms.Textarea(attrs={'rows': 3}),
            'diagnosis': forms.Textarea(attrs={'rows': 3}),
            'treatment_plan': forms.Textarea(attrs={'rows': 3}),
            'follow_up_notes': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class ManipulationForm(forms.ModelForm):
    """Form for procedures/manipulations."""

    class Meta:
        model = Manipulation
        fields = ['name', 'description', 'notes']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control manipulation-autocomplete',
                'data-autocomplete-url': '/visits/manipulation-autocomplete/',
                'autocomplete': 'off',
                'placeholder': 'Въведете наименование на манипулацията',
            }),
            'description': forms.Textarea(attrs={'rows': 2}),
            'notes': forms.Textarea(attrs={'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name != 'name':  # name is already configured
                field.widget.attrs['class'] = 'form-control'


class VaccinationForm(forms.ModelForm):
    """Form for vaccination records."""

    class Meta:
        model = Vaccination
        fields = ['vaccine_name', 'batch_number', 'manufacturer', 'next_due_date', 'notes']
        widgets = {
            'next_due_date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class PrescriptionForm(forms.ModelForm):
    """Form for prescriptions."""

    class Meta:
        model = Prescription
        fields = ['medication', 'dosage', 'frequency', 'duration', 'instructions']
        widgets = {
            'instructions': forms.Textarea(attrs={'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class LabResultForm(forms.ModelForm):
    """Form for lab results."""

    class Meta:
        model = LabResult
        fields = ['title', 'description', 'file']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class AttachmentForm(forms.ModelForm):
    """Form for general attachments."""

    class Meta:
        model = Attachment
        fields = ['title', 'description', 'file']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class DewormingForm(forms.ModelForm):
    """Form for deworming/decontamination records (Обезпаразитяване)."""

    class Meta:
        model = Deworming
        fields = ['product_name', 'dose', 'batch_number', 'manufacturer', 'next_due_date', 'notes']
        widgets = {
            'next_due_date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
