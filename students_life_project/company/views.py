"""
Company app views - Offices and Employees
"""
from django.shortcuts import render, get_object_or_404
from django.utils.translation import gettext_lazy as _
from .models import Office, Employee


def office_list(request):
    """
    List all active offices (Our Team page).
    URL: /team/ or /en/team/
    """
    offices = Office.objects.filter(
        is_active=True
    ).prefetch_related('employees').order_by('order', 'name')
    
    # Get all featured employees for homepage widget
    featured_employees = Employee.objects.filter(
        is_published=True,
        is_featured=True
    ).select_related('office', 'photo').order_by('order', 'last_name')[:8]
    
    return render(request, 'company/office_list.html', {
        'offices': offices,
        'page_title': _('Our Team'),
        'featured_employees': featured_employees,
    })


def office_detail(request, slug):
    """
    Display office detail with employees.
    URL: /team/<slug>/ or /en/team/<slug>/
    """
    office = get_object_or_404(
        Office.objects.filter(is_active=True),
        slug=slug
    )
    
    employees = office.employees.filter(
        is_published=True
    ).select_related('photo').order_by('order', 'last_name', 'first_name')
    
    context = {
        'office': office,
        'employees': employees,
        'page_title': office.name,
    }
    
    return render(request, 'company/office_detail.html', context)


def employee_detail(request, pk):
    """
    Display individual employee profile.
    URL: /team/employee/<pk>/ or /en/team/employee/<pk>/
    """
    employee = get_object_or_404(
        Employee.objects.select_related('office', 'photo').filter(is_published=True),
        pk=pk
    )
    
    # Get other employees from the same office for related section
    related_employees = Employee.objects.filter(
        office=employee.office,
        is_published=True,
        is_featured=False
    ).exclude(pk=employee.pk).select_related('photo').order_by('order', 'last_name')[:4]
    
    context = {
        'employee': employee,
        'related_employees': related_employees,
        'page_title': employee.full_name,
    }
    
    return render(request, 'company/employee_detail.html', context)
