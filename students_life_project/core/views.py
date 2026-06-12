"""
Core app views - Homepage and form handling
"""
import logging
from datetime import datetime
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

from .forms import ContactForm, ConsultationForm
from .form_handlers import FormSubmissionHandler

logger = logging.getLogger(__name__)


def get_client_ip(request):
    """
    Get client IP address from request, handling proxies.
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def home(request):
    """
    Homepage view with context from site_settings context processor.
    Displays featured testimonials, documents, and about sections.
    """
    return render(request, 'core/home.html')


# --- ДОБАВЛЕННЫЕ ОБРАБОТЧИКИ ОШИБОК ДЛЯ ИСПРАВЛЕНИЯ SYSTEMCHECKERROR ---

def custom_404(request, exception):
    """Кастомная страница ошибки 404 (Страница не найдена)"""
    return render(request, 'core/404.html', status=404)


def custom_500(request):
    """Кастомная страница ошибки 500 (Ошибка сервера)"""
    return render(request, 'core/500.html', status=500)

# ----------------------------------------------------------------------


@require_POST
def contact_form_submit(request):
    """
    Handle contact form submission securely on backend.
    Validates data, sends to CRM and Google Sheets.
    """
    form = ContactForm(request.POST)
    
    if form.is_valid():
        # Prepare form data with metadata
        form_data = form.cleaned_data.copy()
        form_data['submitted_at'] = datetime.now().isoformat()
        form_data['ip_address'] = get_client_ip(request)
        form_data['user_agent'] = request.META.get('HTTP_USER_AGENT', '')[:255]
        
        # Submit to external services
        handler = FormSubmissionHandler(form_data)
        results = handler.submit_all(required_fields=['first_name', 'email'])
        
        if results['success']:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'message': _('Thank you! Your message has been sent successfully.')
                })
            else:
                # Redirect with success message
                return redirect('core:contact_success')
        else:
            logger.error(f'Form submission failed: {results["errors"]}')
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'message': _('Sorry, there was an error sending your message. Please try again later.')
                }, status=500)
            else:
                form.add_error(None, _('There was an error submitting your form. Please try again.'))
    
    # Form is invalid
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': False,
            'errors': form.errors
        }, status=400)
    else:
        return render(request, 'core/contact.html', {'form': form})


@require_POST
def consultation_form_submit(request):
    """
    Handle free consultation form submission.
    Similar to contact form but for consultation requests.
    """
    form = ConsultationForm(request.POST)
    
    if form.is_valid():
        form_data = form.cleaned_data.copy()
        form_data['submitted_at'] = datetime.now().isoformat()
        form_data['ip_address'] = get_client_ip(request)
        form_data['user_agent'] = request.META.get('HTTP_USER_AGENT', '')[:255]
        form_data['service_type'] = 'consultation'
        
        handler = FormSubmissionHandler(form_data)
        results = handler.submit_all(required_fields=['first_name', 'email', 'phone'])
        
        if Magic := results['success']:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'message': _('Thank you! We will contact you soon for a free consultation.')
                })
            else:
                return redirect('core:consultation_success')
        else:
            logger.error(f'Consultation form submission failed: {results["errors"]}')
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'message': _('Sorry, there was an error. Please try again later.')
                }, status=500)
            else:
                form.add_error(None, _('There was an error submitting your form. Please try again.'))
    
    # Form is invalid
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': False,
            'errors': form.errors
        }, status=400)
    else:
        return render(request, 'core/consultation.html', {'form': form})


def contact_success(request):
    """Success page after contact form submission"""
    return render(request, 'core/success.html', {
        'title': _('Message Sent'),
        'message': _('Thank you! Your message has been sent successfully. We will contact you soon.')
    })


def consultation_success(request):
    """Success page after consultation form submission"""
    return render(request, 'core/success.html', {
        'title': _('Consultation Requested'),
        'message': _('Thank you! We will contact you soon for a free consultation.')
    })