"""
Core app forms with validation
"""
from django import forms
from django.utils.translation import gettext_lazy as _
from geo.models import Country, City


class ContactForm(forms.Form):
    """
    Contact form for general inquiries.
    Fields are validated on backend and sent to CRM/Google Sheets.
    """
    first_name = forms.CharField(
        label=_('First Name'),
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('Your first name'),
            'required': True
        })
    )
    last_name = forms.CharField(
        label=_('Last Name'),
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('Your last name')
        })
    )
    email = forms.EmailField(
        label=_('Email'),
        max_length=254,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': _('your@email.com'),
            'required': True
        })
    )
    phone = forms.CharField(
        label=_('Phone'),
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+7 (999) 000-00-00'
        })
    )
    country = forms.ChoiceField(
        label=_('Country of Interest'),
        choices=[],
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    city = forms.ChoiceField(
        label=_('City of Interest'),
        choices=[],
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    message = forms.CharField(
        label=_('Message'),
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': _('Your message or question'),
            'rows': 5
        }),
        required=False
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Dynamically populate country choices from database
        countries = Country.objects.filter(is_published=True).order_by('order', 'name')
        country_choices = [('', _('Select a country'))]
        for country in countries:
            country_choices.append((country.slug, country.name))
        self.fields['country'].choices = country_choices
        
        # City choices will be populated via AJAX based on selected country
        self.fields['city'].choices = [('', _('Select a city first'))]
    
    def clean_phone(self):
        """Clean and validate phone number"""
        phone = self.cleaned_data.get('phone', '')
        if phone:
            # Remove common separators
            cleaned = ''.join(c for c in phone if c.isdigit() or c == '+')
            if len(cleaned) < 10:
                raise forms.ValidationError(_('Please enter a valid phone number'))
            return cleaned
        return phone


class ConsultationForm(forms.Form):
    """
    Free consultation request form.
    Requires more fields than contact form.
    """
    SERVICE_TYPE_CHOICES = [
        ('admission', _('University Admission')),
        ('visa', _('Visa Support')),
        ('tour', _('Educational Tour')),
        ('rvp', _('RVP/RVPO')),
        ('other', _('Other')),
    ]
    
    first_name = forms.CharField(
        label=_('First Name'),
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'required': True
        })
    )
    last_name = forms.CharField(
        label=_('Last Name'),
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'required': True
        })
    )
    email = forms.EmailField(
        label=_('Email'),
        max_length=254,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'required': True
        })
    )
    phone = forms.CharField(
        label=_('Phone'),
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'required': True
        })
    )
    service_type = forms.ChoiceField(
        label=_('Service Type'),
        choices=SERVICE_TYPE_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'required': True
        })
    )
    country = forms.ChoiceField(
        label=_('Country of Interest'),
        choices=[],
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    preferred_contact_method = forms.ChoiceField(
        label=_('Preferred Contact Method'),
        choices=[
            ('email', _('Email')),
            ('phone', _('Phone')),
            ('whatsapp', _('WhatsApp')),
            ('telegram', _('Telegram')),
        ],
        initial='phone',
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'})
    )
    comment = forms.CharField(
        label=_('Comment'),
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4
        }),
        required=False
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Populate country choices
        countries = Country.objects.filter(is_published=True).order_by('order', 'name')
        country_choices = [('', _('Select a country'))]
        for country in countries:
            country_choices.append((country.slug, country.name))
        self.fields['country'].choices = country_choices
    
    def clean_phone(self):
        """Clean and validate phone number"""
        phone = self.cleaned_data.get('phone', '')
        cleaned = ''.join(c for c in phone if c.isdigit() or c == '+')
        if len(cleaned) < 10:
            raise forms.ValidationError(_('Please enter a valid phone number'))
        return cleaned
