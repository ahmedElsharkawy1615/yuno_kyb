"""
Forms for merchant registration.
"""
from django import forms
from django.forms import inlineformset_factory
from .models import Merchant, BeneficialOwner, Document


class MerchantRegistrationForm(forms.ModelForm):
    """Form for merchant registration."""

    class Meta:
        model = Merchant
        fields = [
            'business_name',
            'registration_number',
            'country',
            'business_category',
            'email',
            'phone',
            'address',
        ]
        widgets = {
            'business_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter business name'
            }),
            'registration_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter business registration number'
            }),
            'country': forms.Select(attrs={'class': 'form-select'}),
            'business_category': forms.Select(attrs={'class': 'form-select'}),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'business@example.com'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+65 1234 5678'
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter business address'
            }),
        }

    def clean_registration_number(self):
        """Validate registration number is unique."""
        reg_num = self.cleaned_data.get('registration_number')
        if Merchant.objects.filter(registration_number=reg_num).exists():
            raise forms.ValidationError('A merchant with this registration number already exists.')
        return reg_num


class BeneficialOwnerForm(forms.ModelForm):
    """Form for beneficial owner information."""

    class Meta:
        model = BeneficialOwner
        fields = [
            'full_name',
            'nationality',
            'ownership_percentage',
            'id_document_type',
            'id_document_number',
            'is_pep',
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Full legal name'
            }),
            'nationality': forms.Select(
                choices=Merchant.COUNTRY_CHOICES,
                attrs={'class': 'form-select'}
            ),
            'ownership_percentage': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '25.00',
                'min': '0',
                'max': '100',
                'step': '0.01'
            }),
            'id_document_type': forms.Select(attrs={'class': 'form-select'}),
            'id_document_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Document number'
            }),
            'is_pep': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


BeneficialOwnerFormSet = inlineformset_factory(
    Merchant,
    BeneficialOwner,
    form=BeneficialOwnerForm,
    extra=1,
    can_delete=True,
    min_num=0,
    validate_min=False,
)


class DocumentUploadForm(forms.ModelForm):
    """Form for document upload."""

    class Meta:
        model = Document
        fields = ['document_type', 'file']
        widgets = {
            'document_type': forms.Select(attrs={'class': 'form-select'}),
            'file': forms.FileInput(attrs={'class': 'form-control'}),
        }


class MerchantStatusCheckForm(forms.Form):
    """Form to check merchant status."""

    registration_number = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your registration number'
        })
    )
