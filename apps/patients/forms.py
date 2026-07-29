from django import forms
from .models import Patient, WeightRecord
from apps.clients.models import Client


class PatientForm(forms.ModelForm):
    """Form for creating and updating patients."""

    owner = forms.ModelChoiceField(
        queryset=Client.objects.all(),
        label='Собственик',
        widget=forms.Select(attrs={
            'class': 'form-control client-select',
            'data-search-url': '/clients/search/',
        }),
        help_text='Изберете собственик или започнете да пишете за търсене'
    )

    class Meta:
        model = Patient
        fields = [
            'name', 'species', 'breed', 'gender', 'date_of_birth',
            'color', 'microchip_number', 'photo', 'owner',
            'allergies', 'chronic_conditions', 'notes'
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'allergies': forms.Textarea(attrs={'rows': 2}),
            'chronic_conditions': forms.Textarea(attrs={'rows': 2}),
            'notes': forms.Textarea(attrs={'rows': 3}),
            'species': forms.TextInput(attrs={
                'class': 'form-control species-autocomplete',
                'data-autocomplete-url': '/patients/species-autocomplete/',
                'autocomplete': 'off',
                'placeholder': 'напр. Куче, Котка, Птица',
            }),
            'breed': forms.TextInput(attrs={
                'class': 'form-control breed-autocomplete',
                'data-autocomplete-url': '/patients/breed-autocomplete/',
                'autocomplete': 'off',
                'placeholder': 'Въведете порода',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-check-input'
            elif isinstance(field.widget, forms.FileInput):
                field.widget.attrs['class'] = 'form-control'
            elif field_name not in ['owner', 'species', 'breed']:  # already configured
                field.widget.attrs['class'] = 'form-control'


class WeightRecordForm(forms.ModelForm):
    """Form for adding weight records."""

    class Meta:
        model = WeightRecord
        fields = ['weight', 'notes']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
        self.fields['weight'].widget.attrs['placeholder'] = 'Тегло в кг'
        self.fields['notes'].widget.attrs['placeholder'] = 'Незадължителни бележки'
