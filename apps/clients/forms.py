from django import forms
from .models import Client


class ClientForm(forms.ModelForm):
    """Form for creating and updating clients."""

    class Meta:
        model = Client
        fields = ['name', 'phone', 'phone_secondary', 'email', 'address', 'notes']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if isinstance(field.widget, forms.Textarea):
                field.widget.attrs['class'] = 'form-control'
            else:
                field.widget.attrs['class'] = 'form-control'
