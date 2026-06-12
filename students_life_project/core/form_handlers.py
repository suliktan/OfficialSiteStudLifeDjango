"""
Form submission handler - CRM and Google Sheets integration
Secure backend processing with environment variable protection
"""
import requests
import logging
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

logger = logging.getLogger(__name__)


class FormSubmissionHandler:
    """
    Handles form submissions securely on the backend.
    Sends data to CRM API and Google Sheets without exposing credentials to frontend.
    """
    
    def __init__(self, form_data):
        """
        Initialize with validated form data.
        
        Args:
            form_data: dict - Cleaned form data from Django form
        """
        self.form_data = form_data
        self.crm_api_url = settings.CRM_API_URL
        self.crm_api_key = settings.CRM_API_KEY
        self.google_sheets_url = settings.GOOGLE_SHEETS_WEBHOOK_URL
    
    def validate_required_fields(self, required_fields):
        """
        Validate that all required fields are present.
        
        Args:
            required_fields: list - List of required field names
            
        Raises:
            ValidationError: If any required field is missing
        """
        missing_fields = [field for field in required_fields if field not in self.form_data or not self.form_data[field]]
        
        if missing_fields:
            raise ValidationError(
                _('Missing required fields: %(fields)s') % {'fields': ', '.join(missing_fields)}
            )
    
    def send_to_crm(self):
        """
        Send form data to external CRM system via API.
        
        Returns:
            dict: Response from CRM API or error information
        """
        if not self.crm_api_url or not self.crm_api_key:
            logger.warning('CRM API credentials not configured')
            return {
                'success': False,
                'error': 'CRM configuration missing',
                'logged': True
            }
        
        # Prepare payload for CRM
        payload = self._prepare_crm_payload()
        
        headers = {
            'Authorization': f'Bearer {self.crm_api_key}',
            'Content-Type': 'application/json',
            'User-Agent': 'StudentsLife-Django/1.0'
        }
        
        try:
            response = requests.post(
                self.crm_api_url,
                json=payload,
                headers=headers,
                timeout=10  # 10 second timeout
            )
            response.raise_for_status()
            
            logger.info(f'CRM submission successful: {response.status_code}')
            return {
                'success': True,
                'status_code': response.status_code,
                'response': response.json() if response.content else None
            }
            
        except requests.exceptions.Timeout:
            logger.error('CRM API timeout')
            return {'success': False, 'error': 'CRM API timeout'}
        except requests.exceptions.ConnectionError:
            logger.error('CRM API connection error')
            return {'success': False, 'error': 'CRM API connection failed'}
        except requests.exceptions.HTTPError as e:
            logger.error(f'CRM API HTTP error: {e.response.status_code}')
            return {
                'success': False,
                'error': f'CRM API error: {e.response.status_code}',
                'status_code': e.response.status_code
            }
        except Exception as e:
            logger.error(f'Unexpected CRM error: {str(e)}')
            return {'success': False, 'error': str(e)}
    
    def send_to_google_sheets(self):
        """
        Send form data to Google Sheets via webhook.
        
        Returns:
            dict: Response from Google Sheets or error information
        """
        if not self.google_sheets_url:
            logger.warning('Google Sheets webhook URL not configured')
            return {
                'success': False,
                'error': 'Google Sheets configuration missing',
                'logged': True
            }
        
        # Prepare payload for Google Sheets
        payload = self._prepare_google_sheets_payload()
        
        headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'StudentsLife-Django/1.0'
        }
        
        try:
            response = requests.post(
                self.google_sheets_url,
                json=payload,
                headers=headers,
                timeout=10
            )
            response.raise_for_status()
            
            logger.info(f'Google Sheets submission successful: {response.status_code}')
            return {
                'success': True,
                'status_code': response.status_code
            }
            
        except requests.exceptions.Timeout:
            logger.error('Google Sheets webhook timeout')
            return {'success': False, 'error': 'Google Sheets timeout'}
        except requests.exceptions.ConnectionError:
            logger.error('Google Sheets webhook connection error')
            return {'success': False, 'error': 'Google Sheets connection failed'}
        except requests.exceptions.HTTPError as e:
            logger.error(f'Google Sheets HTTP error: {e.response.status_code}')
            return {
                'success': False,
                'error': f'Google Sheets error: {e.response.status_code}'
            }
        except Exception as e:
            logger.error(f'Unexpected Google Sheets error: {str(e)}')
            return {'success': False, 'error': str(e)}
    
    def submit_all(self, required_fields=None):
        """
        Submit form data to all configured destinations.
        
        Args:
            required_fields: list - Optional list of required fields to validate
            
        Returns:
            dict: Combined results from all submissions
        """
        results = {
            'success': True,
            'crm': None,
            'google_sheets': None,
            'errors': []
        }
        
        # Validate required fields if specified
        if required_fields:
            try:
                self.validate_required_fields(required_fields)
            except ValidationError as e:
                results['success'] = False
                results['errors'].append(str(e))
                return results
        
        # Send to CRM
        crm_result = self.send_to_crm()
        results['crm'] = crm_result
        
        if not crm_result.get('success'):
            results['errors'].append(f"CRM: {crm_result.get('error', 'Unknown error')}")
        
        # Send to Google Sheets
        sheets_result = self.send_to_google_sheets()
        results['google_sheets'] = sheets_result
        
        if not sheets_result.get('success'):
            results['errors'].append(f"Google Sheets: {sheets_result.get('error', 'Unknown error')}")
        
        # Overall success if at least one destination succeeded
        results['success'] = crm_result.get('success') or sheets_result.get('success')
        
        return results
    
    def _prepare_crm_payload(self):
        """
        Prepare payload format expected by CRM API.
        Customize this method based on your CRM's API requirements.
        """
        # Map form fields to CRM field names
        return {
            'lead_source': 'website',
            'first_name': self.form_data.get('first_name', ''),
            'last_name': self.form_data.get('last_name', ''),
            'email': self.form_data.get('email', ''),
            'phone': self.form_data.get('phone', ''),
            'country_interest': self.form_data.get('country', ''),
            'city_interest': self.form_data.get('city', ''),
            'service_type': self.form_data.get('service_type', 'admission'),
            'message': self.form_data.get('message', ''),
            'submitted_at': self.form_data.get('submitted_at', ''),
        }
    
    def _prepare_google_sheets_payload(self):
        """
        Prepare payload format for Google Sheets webhook.
        Customize this method based on your Google Apps Script requirements.
        """
        return {
            'timestamp': self.form_data.get('submitted_at', ''),
            'first_name': self.form_data.get('first_name', ''),
            'last_name': self.form_data.get('last_name', ''),
            'email': self.form_data.get('email', ''),
            'phone': self.form_data.get('phone', ''),
            'country': self.form_data.get('country', ''),
            'city': self.form_data.get('city', ''),
            'service_type': self.form_data.get('service_type', ''),
            'message': self.form_data.get('message', ''),
            'ip_address': self.form_data.get('ip_address', ''),
            'user_agent': self.form_data.get('user_agent', ''),
        }
